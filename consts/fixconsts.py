SERVO_PAN_PIN = 48
SERVO_TILT_PIN = 47

LEFT_SONIC_ECHO_PIN = 64  # A10 PK2
LEFT_SONIC_TRIG_PIN = 65  # A11 PK3

RIGHT_SONIC_ECHO_PIN = 60  # A6 PF6
RIGHT_SONIC_TRIG_PIN = 61  # A7 PF7


CLASS_BACKGROUND = 0
CLASS_background = 1
CLASS_car = 2
CLASS_sonic = 3
CLASS_wheel = 4
CLASS_santa = 5
CLASS_wheel_back = 6
CLASS_santa_back = 7

CLASS_ID_TO_NAME = ["BACKGROUND", "background", "car",
                    "sonic", "wheel", "santa", "wheel_back", "santa_back"]

CLASS_NAME_TO_ID = {
    "BACKGROUND": 0,
    "background": 1,
    "car": 2,
    "sonic": 3,
    "wheel": 4,
    "santa": 5,
    "wheel_back": 6,
    "santa_back": 7
}

MAX_ANGLE = 135
MIN_ANGLE = 45

# A B
# C D
#  |
#  V

# Note that A and C is configured backwards

FORWARD_VEC = [-1.0, 1.0, -1.0, 1.0]

BACKWARD_VEC = [1.0, -1.0, 1.0, -1.0]

ROTATE_CLOCKWISE_VEC = [1.0, 1.0, 1.0, 1.0]

ROTATE_ANTICLOCKWISE_VEC = [-1.0, -1.0, -1.0, -1.0]

LEFT_VEC = [-1.0, -1.0, 1.0, 1.0]

RIGHT_VEC = [1.0, 1.0, -1.0, -1.0]


STOP_VEC = [0.0, 0.0, 0.0, 0.0]

MOTOR_NAMES = ["A", "B", "C", "D"]
PWM_PINS = [12, 8, 9, 5]
DIRA_PINS = [34, 37, 43, 58]
DIRB_PINS = [35, 36, 42, 59]

OVERLAY_FLAGS="box,labels,conf"
# OVERLAY_FLAGS = ""

CAM_WIDTH = 1280
CAM_HEIGHT = 720

CAMERA_MATRIX = [[1.35842664e+03, 0.00000000e+00, 6.39752582e+02],
                 [0.00000000e+00, 1.35818081e+03, 3.18681227e+02],
                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

DISTORTION_COEFF = [[-5.90085488e-02,  2.92879222e+00, -9.00343434e-03,  1.42991598e-04,
                     -1.92175429e+01]]
