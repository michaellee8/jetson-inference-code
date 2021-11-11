from typing import List
from pymata4 import pymata4
from time import sleep
from math import floor
from enum import Enum
import jetson.inference
import jetson.utils
from consts.fixconsts import *
from consts.varconsts import *
from pipeline import Pipeline
from source.camera_input import CameraInput
from detector.trt_detector import TrtDetector
from guesser_calculator import GuesserCalculator
from motor_output_calculator import MotorOutputCalculator
from firmata_output import FirmataOutput
from cameradetector import CameraDetector

import argparse
import sys
from os import path

parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.",
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="csi://0",
                    nargs='?', help="URI of the input stream")

parser.add_argument("output_URI", type=str, default="",
                    nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2",
                    help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf",
                    help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.3,
                    help="minimum detection threshold to use")

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

print("capturing", opt.input_URI)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
# output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

print("got video source")

board = pymata4.Pymata4(arduino_instance_id=2)

for pin in DIRA_PINS:
    board.set_pin_mode_digital_output(pin)

for pin in DIRB_PINS:
    board.set_pin_mode_digital_output(pin)

for pin in PWM_PINS:
    board.set_pin_mode_pwm_output(pin)

board.set_pin_mode_servo(SERVO_PAN_PIN)
board.set_pin_mode_servo(SERVO_TILT_PIN)

Pipeline([CameraDetector(input, net).run(), GuesserCalculator().run(
), MotorOutputCalculator(board).run(), FirmataOutput(board).run()]).run_sequential()

board.shutdown()
