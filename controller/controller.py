import mc_control
import mc_rbdyn
import mc_rtc
import mc_tasks
import sva
import eigen
import math

LEFT_HAND_TARGET_POSITION = [0.5, 0.25, 1.1]  # x, y, z
LEFT_HAND_TARGET_ROTATION = [0.7, 0, 0.7, 0]  # w, x, y, z
RIGHT_HAND_TARGET_POSITION = [0.5, -0.25, 1.1]  # x, y, z
RIGHT_HAND_TARGET_ROTATION = [0.7, 0, 0.7, 0]  # w, x, y, z


class Controller(mc_control.MCPythonController):
    def __init__(self, rm, dt):
        self.qpsolver.addConstraintSet(self.kinematicsConstraint)
        self.qpsolver.addConstraintSet(self.contactConstraint)
        self.qpsolver.addConstraintSet(self.selfCollisionConstraint)
        self.qpsolver.addTask(self.postureTask)

        # Left + right feet contacts
        self.addContact(self.robot().name(), "ground", "LeftFoot", "AllGround")
        self.addContact(self.robot().name(), "ground", "RightFoot", "AllGround")

        # Hands tasks
        self.left_hand_task = mc_tasks.EndEffectorTask(
            "l_wrist", self.robots(), 0, 10.0, 1000.0
        )
        self.right_hand_task = mc_tasks.EndEffectorTask(
            "r_wrist", self.robots(), 0, 10.0, 1000.0
        )
        self.qpsolver.addTask(self.left_hand_task)
        self.qpsolver.addTask(self.right_hand_task)
        self.left_hand_original_position = self.left_hand_task.get_ef_pose()
        self.right_hand_original_position = self.right_hand_task.get_ef_pose()

        # Head roll
        self.head_pitch_joint_index = self.robot().jointIndexByName("NECK_P")

        self.animation_step = -1

    def update_targets(self):
        # Left hand up
        if self.animation_step == 0:
            print("Left hand going up...")
            self.left_hand_task.set_ef_pose(
                sva.PTransformd(
                    eigen.Quaterniond(*LEFT_HAND_TARGET_ROTATION),
                    eigen.Vector3d(*LEFT_HAND_TARGET_POSITION),
                )
            )

            # Head up
            self.postureTask.target(
                {b"NECK_P": self.robot().ql[self.head_pitch_joint_index]}
            )

        # Left hand down
        elif self.animation_step == 1:
            print("Left hand going down...")
            self.left_hand_task.set_ef_pose(self.left_hand_original_position)

            # Head down
            self.postureTask.target(
                {b"NECK_P": self.robot().qu[self.head_pitch_joint_index]}
            )

        # Right hand up
        elif self.animation_step == 2:
            print("Right hand going up...")
            self.right_hand_task.set_ef_pose(
                sva.PTransformd(
                    eigen.Quaterniond(*RIGHT_HAND_TARGET_ROTATION),
                    eigen.Vector3d(*RIGHT_HAND_TARGET_POSITION),
                )
            )

            # Head up
            self.postureTask.target(
                {b"NECK_P": self.robot().ql[self.head_pitch_joint_index]}
            )

        # Right hand down
        elif self.animation_step == 3:
            print("Right hand going down...")
            self.right_hand_task.set_ef_pose(self.right_hand_original_position)

            # Head down
            self.postureTask.target(
                {b"NECK_P": self.robot().qu[self.head_pitch_joint_index]}
            )

        # Both hands up
        elif self.animation_step == 4:
            print("Both hands going up...")
            self.left_hand_task.set_ef_pose(
                sva.PTransformd(
                    eigen.Quaterniond(*LEFT_HAND_TARGET_ROTATION),
                    eigen.Vector3d(*LEFT_HAND_TARGET_POSITION),
                )
            )
            self.right_hand_task.set_ef_pose(
                sva.PTransformd(
                    eigen.Quaterniond(*RIGHT_HAND_TARGET_ROTATION),
                    eigen.Vector3d(*RIGHT_HAND_TARGET_POSITION),
                )
            )

            # Head default
            self.postureTask.target({b"NECK_P": [0.1]})

        # Both hands down
        elif self.animation_step == 5:
            print("Both hands going down...")
            self.left_hand_task.set_ef_pose(self.left_hand_original_position)
            self.right_hand_task.set_ef_pose(self.right_hand_original_position)

            # Head default
            self.postureTask.target({b"NECK_P": [-0.1]})

    def run_callback(self):
        # If both tasks reached their target precisions, procede to the next animation step
        if (
            self.left_hand_task.eval().norm() < 0.01
            and self.right_hand_task.eval().norm() < 0.01
        ):
            self.animation_step = (
                self.animation_step + 1
            ) % 6  # We only have 6 animation steps
            print(f"Animation step updated to {self.animation_step}!")
            self.update_targets()

        return True

    def reset_callback(self, data):
        self.left_hand_task.reset()
        self.right_hand_task.reset()
        pass

    @staticmethod
    def create(robot, dt):
        env = mc_rbdyn.get_robot_module("env", mc_rtc.MC_ENV_DESCRIPTION_PATH, "ground")
        return Controller([robot, env], dt)
