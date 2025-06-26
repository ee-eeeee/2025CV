import cv2
import numpy as np
import pandas as pd
from all_model import *


def get_it_array(X_train):
    # 确保是 NumPy 数组
    if not isinstance(X_train, np.ndarray):
        X_train = np.array(X_train)

    return X_train


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def computeStrain(u, v):
    u_x = u - pd.DataFrame(u).shift(-1, axis=1)
    v_y = v - pd.DataFrame(v).shift(-1, axis=0)
    u_y = u - pd.DataFrame(u).shift(-1, axis=0)
    v_x = v - pd.DataFrame(v).shift(-1, axis=1)
    os = np.array(np.sqrt(u_x**2 + v_y**2 + 1/2 * (u_y+v_x)**2).ffill(axis=1).ffill(axis=0))
    return os


def calculate_optical_flow(frame1, frame2):

    optical_flow = cv2.optflow.DualTVL1OpticalFlow_create()
    flow = optical_flow.calc(frame1, frame2, None)
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    u, v = pol2cart(magnitude, angle)
    os_ = computeStrain(u, v)

    final_u = cv2.resize(u, (48, 48))
    final_v = cv2.resize(v, (48, 48))
    final_os = cv2.resize(os_, (48, 48))

    if (np.max(final_u) - np.min(final_u))==0:
        normalized_u = final_u.astype(np.uint8)
    else:
        normalized_u = ((final_u - np.min(final_u)) / (np.max(final_u) - np.min(final_u)) * 255).astype(np.uint8)

    if (np.max(final_v) - np.min(final_v))==0:
        normalized_v = final_v.astype(np.uint8)
    else:
        normalized_v = ((final_v - np.min(final_v)) / (np.max(final_v) - np.min(final_v)) * 255).astype(np.uint8)

    if (np.max(final_os) - np.min(final_os))==0:
        normalized_os = final_os.astype(np.uint8)
    else:
        normalized_os = ((final_os - np.min(final_os)) / (np.max(final_os) - np.min(final_os)) * 255).astype(np.uint8)

    return normalized_u, normalized_v, normalized_os


def count_optflow(imgs):

    if len(imgs[0].shape) == 3:
        imgs[0] = normalize_gray(imgs[0])
        imgs[1] = normalize_gray(imgs[1])
        imgs[2] = normalize_gray(imgs[2])
    optflows = []

    if imgs[0].dtype != imgs[1].dtype:
        imgs[0] = imgs[0].astype(imgs[1].dtype)
        imgs[2] = imgs[2].astype(imgs[1].dtype)

    flow_1_u, flow_1_v, flow_1_os = calculate_optical_flow(imgs[0], imgs[1])
    flow_2_u, flow_2_v, flow_2_os = calculate_optical_flow(imgs[1], imgs[2])

    optflows.append(normalize_gray(flow_1_u))
    optflows.append(normalize_gray(flow_1_v))
    optflows.append(normalize_gray(flow_2_u))
    optflows.append(normalize_gray(flow_2_v))

    return optflows


def normalize_gray(images):
    if len(images.shape) == 3:
        images = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    images = cv2.normalize(images, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return images


class EmotionRecognizer:
    def __init__(self):
        # 加载预训练的情绪识别模型
        self.model = self.load_emotion_model()
        # self.model.eval()
        self.emotion_labels = ["others", "happiness", "sadness", "surprise", "disgust", "repression", "fear"]
        
    def load_emotion_model(self):
        # 加载你的预训练情绪识别模型
        # 这里需要替换为实际模型文件路径
        try:
            model = get_model(class_num=7, alpha=2).to('cuda')
            # model.load_state_dict(torch.load("./skd-tstsan.pth"))

            # state_dict = torch.load("./skd-tstsan.pth")
            state_dict = torch.load("./sub01.pth")
            filtered_dict = {k: v for k, v in state_dict.items() if "fc" not in k}
            model.load_state_dict(filtered_dict, strict=False)

            return model
        except Exception as e:
            print(f"加载情绪识别模型失败: {e}")
            return None
        
    def recognize_emotion(self, input_images):
        # 预处理人脸图像
        processed_face = self.load_image(input_images).to("cuda")
        if processed_face is None:
            return "无法识别"
            
        # 使用模型预测情绪
        yhat, AC1_out, AC2_out, final_feature, AC1_feature, AC2_feature = self.model(processed_face)
        # print(yhat)
        # print(yhat.shape)
        max_index = np.argmax(yhat.detach().cpu())
        max_in = torch.max(yhat, 1)[1]
        
        # 返回对应的情绪标签
        return max_in

    def load_image(self, imgs):

        end_input = []

        large_S_apex = normalize_gray(imgs[1])
        large_S_onset = normalize_gray(imgs[0])
        small_S_apex = cv2.resize(large_S_apex, (48, 48))
        small_S_onset = cv2.resize(large_S_onset, (48, 48))
        end_input.append(small_S_apex)
        end_input.append(small_S_onset)

        grid_sizes = [4]
        for grid_size in grid_sizes:
            height, width = large_S_apex.shape
            block_height, block_width = height // grid_size, width // grid_size

            for i in range(grid_size):
                for j in range(grid_size):
                    block = large_S_apex[i * block_height: (i + 1) * block_height,
                            j * block_width: (j + 1) * block_width]

                    scaled_block = cv2.resize(block, (48, 48))

                    end_input.append(scaled_block)

        for grid_size in grid_sizes:
            height, width = large_S_onset.shape
            block_height, block_width = height // grid_size, width // grid_size

            for i in range(grid_size):
                for j in range(grid_size):
                    block = large_S_onset[i * block_height: (i + 1) * block_height,
                            j * block_width: (j + 1) * block_width]

                    scaled_block = cv2.resize(block, (48, 48))

                    end_input.append(scaled_block)

        optflows = count_optflow(imgs)

        for img in optflows:
            end_input.append(normalize_gray(img))

        end_input = np.stack(end_input, axis=-1)
        end_input = get_it_array(end_input)

        # end_input = torch.Tensor(end_input).permute(2, 0, 1)
        end_input = torch.Tensor(end_input).unsqueeze(0).permute(0, 3, 1, 2)
        return end_input
