from consts.fixconsts import *
from consts.varconsts import *
from detector.trt_detector import DetectorOutput
from typing import Any, Generator
from typing import Generator, NewType, Any, Tuple, List, Optional
from utils import Side

# from tail of the car
# clockwise is +, anti-clockwise is 360-
# guessed_car_side is NONE if car not found
# ((x_diff, y_diff, z_diff), angle_diff, guessed_car_side, cam_x_diff, timestamp)
# cam_x_diff is + for right
GuesserCalculatorOutput = Tuple[Optional[Tuple[float,
                                               float, float]], Optional[float], Side, float, int]


def x_cen(box: List[float]) -> float:
    return (box[0][0] + box[0][2]) / 2


def y_cen(box: List[float]) -> float:
    return (box[0][1] + box[0][3]) / 2


def x_size(box: List[float]) -> float:
    return box[0][0] - box[0][2]


def y_size(box: List[float]) -> float:
    return box[0][1] - box[0][3]


def area(box: List[float]) -> float:
    return x_size(box) * y_size(box)

def best_det(dets: List[Tuple[Tuple[int, int, int, int], int, float]]) -> Optional[Tuple[Tuple[int, int, int, int], int, float]]:
    if len(dets) == 0:
        return None
    return max(dets, key=lambda d: d[2])


class GuesserCalculator(object):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> Generator[GuesserCalculatorOutput, DetectorOutput, None]:
        (detections, timestamp) = yield
        # ([((box_x1, box_y1, box_x2, box_y2), labelId, probs)], timestamp)
        while True:
            # check for car exists first
            car_dets = [det for det in detections if det[1] == CLASS_car]

            front_santa_dets = [det for det in detections if det[1] == CLASS_santa]
            back_santa_dets = [det for det in detections if det[1] == CLASS_santa_back]
            both_santa_dets = front_santa_dets + back_santa_dets

            back_wheel_dets = [det for det in detections if det[1] == CLASS_wheel_back]
            front_wheel_dets = [det for det in detections if det[1] == CLASS_wheel]
            both_wheel_dets = front_wheel_dets + back_wheel_dets

            sonar_dets = [det for det in detections if det[1] == CLASS_sonic]

            cam_x_diff = 0.0

            # make sure we know if we are using santa_det as car_det
            has_car_det = len(car_dets) > 0
            has_front_santa_det = len(front_santa_dets) > 0
            has_back_santa_det = len(back_santa_dets) > 0
            has_both_santa_det = len(both_santa_dets) > 0
            has_back_wheel_det = len(back_wheel_dets) > 0
            has_front_wheel_det = len(front_wheel_dets) > 0
            has_both_wheel_det = len(both_wheel_dets) > 0
            has_sonar_det = len(sonar_dets) > 0

            front_santa_det = best_det(front_santa_dets)
            back_santa_det = best_det(back_santa_dets)
            both_santa_det = best_det(both_santa_dets)
            back_wheel_det = best_det(back_wheel_dets)
            front_wheel_det = best_det(front_wheel_dets)
            both_wheel_det = best_det(both_wheel_dets)
            sonar_det = best_det(sonar_dets)


            # Use santa for fallback if cannot find car
            if len(car_dets) < 1 and len(both_santa_dets) < 1:
                result = (None, 0, Side.NONE, 0.0, timestamp)
                (detections, timestamp) = yield result
                continue
            # Select for car/santa with highest prob
            car_det = best_det(car_dets) if len(
                car_dets) > 0 else best_det(both_santa_dets)
            car_side = Side.NONE
            if x_cen(car_det) < CAM_WIDTH / 2:
                car_side = Side.LEFT
            else:
                car_side = Side.RIGHT
            cam_x_diff = x_cen(car_det) - CAM_WIDTH / 2
            guessed_car_angle = None
            if has_car_det and front_santa_det != None and abs(x_cen(front_santa_det) - x_cen(car_det)) / CAM_WIDTH < 0.15:
                # we have the back
                guessed_car_angle = 0
            elif has_car_det and back_santa_det != None and abs(x_cen(back_santa_det) - x_cen(car_det)) / CAM_WIDTH < 0.15:
                # We have the front, going to crash!
                guessed_car_angle = 180
            elif front_santa_det != None and front_wheel_det != None:
                if x_cen(front_santa_det) > x_cen(front_wheel_det):
                    guessed_car_angle = 315
                else:
                    guessed_car_angle = 45
            elif back_santa_det != None and front_wheel_det != None and sonar_det != None:
                if x_cen(sonar_det) < x_cen(front_santa_det):
                    guessed_car_angle = 225
                else:
                    guessed_car_angle = 135
            else:
                guessed_car_angle = 0
            
            (detections, timestamp) = yield (None, guessed_car_angle, car_side, cam_x_diff, timestamp)
