#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

import time

from hardware_config import OUT_REVERSE, OUT_SPD, OUT_THROTTLE, IN_KEY_ENTER, IN_KEY_LEFT, IN_KEY_RIGHT, LCD_ADDR, LCD_WIDTH, LCD_HEIGHT
from tachometer import Tachometer


if __name__ == "__main__":
    tester = Tachometer()
    print("Start...")

    while(True):
        print("=> Pulse time W:{} V:{} U:{}".format(tester.pulseTimeW, tester.pulseTimeV, tester.pulseTimeU))
        print("=> Pulse count W:{} V:{} U:{}".format(tester.pulseCountW, tester.pulseCountV, tester.pulseCountU))
        print("=> rotation : " + str(tester.direct))
        time.sleep(1)
