import numpy as np
from enum import Enum


class ActionStatus(Enum):
    Others = 0
    PutDown = 1
    Raised = 2

class SportLog_armsSideways:
    def __init__(self):
        # 初始化动作状态、是否满足条件a和完成动作的个数
        self.current_action_status = ActionStatus.Others  # 当前动作状态，如"unknown"、"started"、"completed"等
        self.isRaised = False  # 是否满足条件a
        self.action_count = 0  # 完成动作的个数

    def update_status(self, joint_coords):
        # 定义左右两边脚腕、肩膀、髋关节的坐标
        coord_ankle_l_y = joint_coords[27].y
        coord_ankle_r_y = joint_coords[28].y

        coord_shoulder_l_y = joint_coords[11].y
        coord_shoulder_r_y = joint_coords[12].y

        coord_hip_l_y = joint_coords[23].y
        coord_hip_r_y = joint_coords[24].y

        coord_knee_l_y = joint_coords[25].y
        coord_knee_r_y = joint_coords[26].y

        # 比较手腕和肩膀的纵轴坐标，看差值是否在10%以内
        # 检查是否满足站立的要求
        if (abs(coord_shoulder_l_y - 2*coord_hip_l_y + coord_ankle_l_y)<0.3 and abs(
                coord_shoulder_r_y - 2*coord_hip_r_y + coord_ankle_r_y)<0.3 and coord_hip_l_y
                < coord_knee_l_y-0.1 and coord_hip_r_y < coord_knee_r_y-0.1):
            self.current_action_status = ActionStatus.Raised
            print("stand",abs(coord_shoulder_l_y - 2*coord_hip_l_y + coord_ankle_l_y))
            return

        # 差值大于9%，则比较手腕和髋关节纵轴坐标，看差值是否在3%以内
        if coord_hip_l_y > coord_knee_l_y-0.1 and coord_hip_r_y > coord_knee_r_y-0.1:
            self.current_action_status = ActionStatus.PutDown
            print("down")
            return

        #两者都不满足，设置当前状态为其他
        self.current_action_status = ActionStatus.Others
        abs(coord_shoulder_l_y - 2 * coord_ankle_l_y + coord_hip_l_y)
        print("no:",abs(coord_shoulder_l_y - 2 * coord_ankle_l_y + coord_hip_l_y))
        return

    def work(self):
        if self.current_action_status == ActionStatus.Raised :
            self.isRaised = True
            return
        elif self.current_action_status == ActionStatus.PutDown :
            if self.isRaised:
                self.isRaised=False
                self.action_count = self.action_count + 1
            return
        else:
            return


    def get_action_count(self):
        """
        返回动作完成的个数
        :return: 动作完成的个数
        """
        return self.action_count
