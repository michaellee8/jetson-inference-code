from math import floor
from typing import Tuple
from utils import times_list, sum_list
from utils import Side
from consts.fixconsts import *
from consts.varconsts import *
from typing import Any, Generator
from typing import Generator, NewType, Any, Tuple, List, Optional
from pymata4 import pymata4
from motor_output_calculator import MotorOutputCalculatorOutput

def execute_movement_vector(board: pymata4.Pymata4, vec: List[float]):
    for motor_index in range(4):
        outn = int(floor(vec[motor_index] * NORMAL_PWM))
        if outn > 0:
            board.digital_write(DIRA_PINS[motor_index], 0)
            board.digital_write(DIRB_PINS[motor_index], 1)
        else:
            board.digital_write(DIRA_PINS[motor_index], 1)
            board.digital_write(DIRB_PINS[motor_index], 0)
        outn = int(abs(outn))
        board.pwm_write(PWM_PINS[motor_index], outn)
    return


def clamp_angle(angle: int) -> int:
    if angle < MIN_ANGLE:
        return MIN_ANGLE
    if angle > MAX_ANGLE:
        return MAX_ANGLE
    return angle


def execute_pan_angle(board: pymata4.Pymata4, angle: int):
    current_pan_angle = angle
    board.servo_write(SERVO_PAN_PIN, clamp_angle(angle))

def execute_tilt_angle(board: pymata4.Pymata4, angle: int):
    current_tilt_angle = angle
    board.servo_write(SERVO_TILT_PIN, clamp_angle(angle))

class FirmataOutput(object):

    def __init__(self, board: pymata4.Pymata4) -> None:
        super().__init__()
        self.board = board

    def run(self) -> Generator[None, MotorOutputCalculatorOutput, None]:
        (mov_A, mov_B, mov_C, mov_D, pan_angle, tilt_angle, timestamp) = yield
        while True:
            clamped_pan_angle = clamp_angle(round(pan_angle))
            clamped_tilt_angle = clamp_angle(round(tilt_angle))
            execute_pan_angle(self.board, clamped_pan_angle)
            execute_tilt_angle(self.board, clamped_tilt_angle)
            execute_movement_vector(self.board, [mov_A, mov_B, mov_C, mov_D])
            (mov_A, mov_B, mov_C, mov_D, pan_angle, tilt_angle, timestamp) = yield
