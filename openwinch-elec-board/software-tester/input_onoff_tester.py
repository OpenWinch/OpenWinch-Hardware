#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from gpiozero import Button
import time

GPIO = 11

i = 0
input = Button(GPIO)  # , pull_up=False)


def trigger():
    global i
    i = i + 1
    print("Up ! {}".format(i))


print("Start...")
input.when_pressed = trigger

while(True):
    time.sleep(99999)

