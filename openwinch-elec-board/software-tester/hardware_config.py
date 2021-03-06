#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

# I2C
I2C_SDA = 2
I2C_SLC = 3

# UART
UART_TX = 14
UART_RX = 15

# Reverse/Init(hold)
IN_KEY_ENTER = 7

# Move Left
IN_KEY_LEFT = 25
IN_KEY_RIGHT = 8

# Reverse
OUT_REVERSE = 9

# Speed Mode
OUT_SPD = 11
OUT_PWR = 25

# Throttle
OUT_THROTTLE = 18

# Tachometer
IN_HS_W = 23
IN_HS_V = 24
IN_HS_U = 4

# LCD
LCD_WIDTH = 128
LCD_HEIGHT = 64
LCD_ADDR = 0x3c

LCD_FPS = 10