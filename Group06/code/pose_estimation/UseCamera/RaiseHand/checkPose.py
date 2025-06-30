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
        # 定义左右两边手腕、肩膀、髋关节的坐标
        coord_wrist_l_x=joint_coords[15].x
        coord_wrist_l_y = joint_coords[15].y
        coord_wrist_l_z = joint_coords[15].z
        coord_wrist_r_x = joint_coords[16].x
        coord_wrist_r_y = joint_coords[16].y
        coord_wrist_r_z = joint_coords[16].z

        coord_shoulder_l_x = joint_coords[11].x
        coord_shoulder_l_y = joint_coords[11].y
        coord_shoulder_l_z = joint_coords[11].z
        coord_shoulder_r_x = joint_coords[12].x
        coord_shoulder_r_y = joint_coords[12].y
        coord_shoulder_r_z = joint_coords[12].z

        coord_hip_l_x = joint_coords[23].x
        coord_hip_l_y = joint_coords[23].y
        coord_hip_l_z = joint_coords[23].z
        coord_hip_r_x = joint_coords[24].x
        coord_hip_r_y = joint_coords[24].y
        coord_hip_r_z = joint_coords[24].z

        # 比较手腕和肩膀的纵轴坐标，看差值是否在9%以内
        if abs(coord_shoulder_l_y-coord_wrist_l_y)<0.09 and abs(
                coord_shoulder_r_y-coord_wrist_r_y)<0.09:
            self.current_action_status = ActionStatus.Raised
            return

        # 差值大于9%，则比较手腕和髋关节纵轴坐标，看差值是否在3%以内
        if abs(coord_hip_l_y-coord_wrist_l_y)<0.03 and abs(
                coord_hip_r_y-coord_wrist_r_y)<0.03:
            self.current_action_status = ActionStatus.PutDown
            return

        #两者都不满足，设置当前状态为其他
        self.current_action_status = ActionStatus.Others
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
