import os

sets = ['train', 'val']

labels_path = "dataset/labels"
txt_path = "dataset/labels"

for image_set in sets:
    image_i = []

    for image_ids in os.listdir(labels_path + '/%s' % (image_set)):
        _name = image_ids.split(".")[0]
        image_i.append(_name)
    list_file = open(txt_path + '/%s.txt' % (image_set), 'a')
    for c_id in image_i:
        print(c_id)
        list_file.write('dataset/images' + '/%s/%s.jpg\n' % (image_set, c_id))
        # 注意，这里我的路径E:\yolov8Project\ultralytics\dataset\images是指代的yolov8项目中图片的目录位置
    list_file.close()