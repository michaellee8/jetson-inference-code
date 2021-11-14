"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import sys
import time
from pymata4 import pymata4

"""
This program continuously monitors an HC-SR04 Ultrasonic Sensor
It reports changes to the distance sensed.
"""
# indices into callback data
DISTANCE_CM = 2
ECHO_PIN = 64
TRIGGER_PIN = 65

LEFT_SONIC_ECHO_PIN = 64  # A10 PK2
LEFT_SONIC_TRIG_PIN = 65  # A11 PK3

RIGHT_SONIC_ECHO_PIN = 60  # A6 PF6
RIGHT_SONIC_TRIG_PIN = 61  # A7 PF7


# A callback function to display the distance
def the_callback(data):
    """
    The callback function to display the change in distance
    :param data: [pin_type=12, trigger pin number, distance, timestamp]
    """
    # print(f'Distance in cm: {data[DISTANCE_CM]}')
    print(f'data: {data}')


def sonar(my_board, trigger_pin, echo_pin, callback):
    """
    Set the pin mode for a sonar device. Results will appear via the
    callback.
    :param my_board: an pymata express instance
    :param trigger_pin: Arduino pin number
    :param echo_pin: Arduino pin number
    :param callback: The callback function
    """

    # set the pin mode for the trigger and echo pins
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)
    # wait forever



board = pymata4.Pymata4(arduino_instance_id=2)
try:
    sonar(board, LEFT_SONIC_TRIG_PIN, LEFT_SONIC_ECHO_PIN, the_callback)
    sonar(board, RIGHT_SONIC_TRIG_PIN, RIGHT_SONIC_ECHO_PIN, the_callback)
    while True:
        try:
            time.sleep(1)
            # print(f'data read: {my_board.sonar_read(TRIGGER_PIN)}')
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)
    board.shutdown()
except (KeyboardInterrupt, RuntimeError):
    board.shutdown()
    sys.exit(0)