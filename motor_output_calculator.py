from typing import Tuple
from utils import times_list, sum_list

from utils import Side
from consts.fixconsts import *
from consts.varconsts import *
from guesser_calculator import GuesserCalculatorOutput
from typing import Any, Generator
from typing import Generator, NewType, Any, Tuple, List, Optional
from pymata4 import pymata4

# (mov_A, mov_B, mov_C, mov_D, pan_angle, tilt_angle, timestamp)
MotorOutputCalculatorOutput = Tuple[float,
                                    float, float, float, float, float, int]


class MotorOutputCalculator(object):
    def __init__(self, board: pymata4.Pymata4) -> None:
        super().__init__()
        # Hack to get board here so that we can get sonar value
        # Do not set sonar pin mode in init!
        self.board = board
        self.left_sonar_distance = 0.0
        self.right_sonar_distance = 0.0
        self.cur_tilt_angle = 90.0
        self.cur_pan_angle = 90.0
        self.prev_seen_car = Side.NONE
        board.set_pin_mode_sonar(
            LEFT_SONIC_TRIG_PIN, LEFT_SONIC_ECHO_PIN, self.sonar_callback)
        board.set_pin_mode_sonar(RIGHT_SONIC_TRIG_PIN,
                                 RIGHT_SONIC_ECHO_PIN, self.sonar_callback)

    def sonar_callback(self, data) -> None:
        (_, pin_n, dist, _) = data
        if pin_n == LEFT_SONIC_TRIG_PIN:
            self.left_sonar_distance = dist
            print("sonar_left", dist)
        elif pin_n == RIGHT_SONIC_TRIG_PIN:
            print("sonar_right", dist)
            self.right_sonar_distance = dist

    def run(self) -> Generator[MotorOutputCalculatorOutput, GuesserCalculatorOutput, None]:

        # ignore predicted pos_diff for now
        (_, angle_diff, guessed_car_side, cam_x_diff, timestamp) = yield

        while True:

            mov_vec = [0.0, 0.0, 0.0, 0.0]

            if guessed_car_side == Side.NONE:
                # Car not found!
                # rotate wiwthout translation to find car
                rot_vec = ROTATE_CLOCKWISE_VEC
                if self.prev_seen_car == Side.RIGHT:
                    pass
                elif self.prev_seen_car == Side.LEFT:
                    rot_vec = times_list(rot_vec, -1)
                else:
                    # Choose clockwise if we have never seen the car anyway
                    pass
                mov_vec = times_list(rot_vec, NOT_SEEN_ROTATION_SPEED)
                (_, angle_diff, guessed_car_side, cam_x_diff, timestamp) = yield (mov_vec[0], mov_vec[1], mov_vec[2], mov_vec[3], self.cur_pan_angle, self.cur_tilt_angle, timestamp)
                continue
            self.prev_seen_car = guessed_car_side
            next_pan_angle = self.cur_pan_angle
            next_tilt_angle = self.cur_tilt_angle

            if cam_x_diff > CAM_WIDTH * 0.1:
                next_pan_angle += 30 * abs(cam_x_diff) / (CAM_WIDTH / 2)
            elif cam_x_diff < CAM_WIDTH * 0.1:
                next_pan_angle -= 30 * abs(cam_x_diff) / (CAM_WIDTH / 2)
            else:
                # car at camera center, very good!
                pass

            mov_vec = times_list(BACKWARD_VEC, FORWARD_COEFFICIENT * 0.5)
            # estimated_angle_diff = (
                # self.cur_pan_angle - 90 + 30 * cam_x_diff / (CAM_WIDTH/2)) % 360.0
            estimated_angle_diff = (
                self.cur_pan_angle - 90 + 30 * cam_x_diff / (CAM_WIDTH/2)) % 360.0 + angle_diff
            estimated_angle_diff = estimated_angle_diff / 2
            rot_vec = times_list(ROTATE_CLOCKWISE_VEC, (estimated_angle_diff - 360 if estimated_angle_diff > 180 else estimated_angle_diff) * ROTATE_COEFFICIENT / 180 *  0.2)
            # rot_vec = [0.0, 0.0, 0.0, 0.0]
            mov_vec = sum_list(mov_vec, rot_vec)

        

            if self.left_sonar_distance < DESIRED_DISTANCE or self.right_sonar_distance < DESIRED_DISTANCE:
                print(self.left_sonar_distance, self.right_sonar_distance)
                mov_vec = times_list(mov_vec, 0.25)

            (_, angle_diff, guessed_car_side, cam_x_diff, timestamp) = yield (mov_vec[0], mov_vec[1], mov_vec[2], mov_vec[3], next_pan_angle, next_tilt_angle, timestamp)
