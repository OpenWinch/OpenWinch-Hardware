#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

import time

from gpiozero import LED

DELAY = 1
GPIO = 11

output = LED(GPIO)

print("Start...")
while(True):
    print("On !")
    output.on()
    time.sleep(DELAY)

    print("Off !")
    output.off()
    time.sleep(DELAY)
