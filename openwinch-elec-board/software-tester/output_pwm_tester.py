#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

import time

from gpiozero import PWMOutputDevice

DELAY = 1
GPIO = 18
INC = 1
MIN = 0
MAX = 1

output = PWMOutputDevice(GPIO)

print("Start...")
output.value = 0
output.on()

i_inc = INC
i = 0
while(True):
    floating = i * 0.1
    print("Value : {}".format(floating))
    output.value = floating

    i = i + i_inc
    if (i >= MAX):
        i_inc = -INC

    if (i <= MIN):
        i_inc = INC

    time.sleep(DELAY)
