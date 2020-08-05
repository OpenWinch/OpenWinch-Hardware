#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from gpiozero import Button

from hardware_config import IN_HS_W, IN_HS_V, IN_HS_U
from constantes import MOTOR_PPR, WINCH_DIAM

CW = 1      # Assign a value to represent clock wise rotation
CCW = -1    # Assign a value to represent counter-clock wise rotation

PPR = 90


millis = lambda: int(round(time.time() * 1000))


class Tachometer(object):

    direct = CW
    RPM = 0
    KPM = 0

    # Sensor
    hsw = Button(IN_HS_W)
    hsv = Button(IN_HS_V)
    hsu = Button(IN_HS_U)

    pulseTimeW = 0
    pulseTimeV = 0
    pulseTimeU = 0

    pulseCountW = 0
    pulseCountV = 0
    pulseCountU = 0

    startTimeW = millis()
    startTimeV = millis()
    startTimeU = millis()

    prevTimeW = 0
    prevTimeV = 0
    prevTimeU = 0

    rpmW = 0
    rpmV = 0
    rpmU = 0

    kpmW = 0
    kpmV = 0
    kpmU = 0

    def __init__(self):
        self.hsw.when_pressed = self.hallSensorW
        self.hsv.when_pressed = self.hallSensorV
        self.hsu.when_pressed = self.hallSensorU


    # def __HallSensor(self):
    #     global pulseCount, RPM

    #     pulseCount = pulseCount + (1 * direct)                      # Add 1 to the pulse count
    #     AvPulseTime = ((pulseTimeW + pulseTimeU + pulseTimeV) / 3)  # Calculate the average time between pulses
    #     PPM = (1000 / AvPulseTime) * 60                             # Calculate the pulses per min (1000 millis in 1 second)
    #     RPM = PPM / PPR                                             # Calculate revs per minute based on number of pulses per rev

    # def get_rpm(self):

    #     delta = delta / 60
    #     self.rpm = (self.hsw_count / delta) / MOTOR_PPR

    def hallSensorW(self):
        # Set startTime to current microcontroller elapsed time value
        self.startTimeW = millis()

        # Read the current W hall sensor value
        __HSW_Val = self.hsw.is_pressed()
        # Read the current V (or U) hall sensor value
        __HSV_Val = self.hsv.is_pressed()
        # Determine rotation direction (ternary if statement)
        self.direct = CW if __HSW_Val == __HSV_Val else CCW

        # Calculate the current time between pulses W
        self.pulseTimeW = self.startTimeW - self.prevTimeW
        # Remember the start time for the next interrupt
        self.prevTimeW = self.startTimeW

        self.pulseCountW = self.pulseCountW + (1 * self.direct)

    def hallSensorV(self):
        self.startTimeV = millis()

        __HSV_Val = self.hsv.is_pressed()
        __HSU_Val = self.hsu.is_pressed()
        self.direct = CW if __HSV_Val == __HSU_Val else CCW

        self.pulseTimeV = self.startTimeV - self.prevTimeV
        self.__HallSensor()
        self.prevTimeV = self.startTimeV

        self.pulseCountV = self.pulseCountV + (1 * self.direct)

    def hallSensorU(self):
        self.startTimeU = millis()

        __HSU_Val = self.hsu.is_pressed()
        __HSW_Val = self.hsw.is_pressed()
        self.direct = CW if __HSU_Val == __HSW_Val else CCW

        self.pulseTimeU = self.startTimeU - self.prevTimeU
        self.__HallSensor()
        self.prevTimeU = self.startTimeU

        self.pulseCountU = self.pulseCountU + (1 * self.direct)

    def get_Direction(self):
        return self.direct
