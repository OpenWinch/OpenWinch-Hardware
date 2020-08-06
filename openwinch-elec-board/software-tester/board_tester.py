
import time
import atexit
import curses

from hardware_config import (
    OUT_REVERSE,
    OUT_SPD,
    OUT_THROTTLE,
    IN_KEY_ENTER,
    IN_KEY_LEFT,
    IN_KEY_RIGHT,
    LCD_ADDR,
    LCD_WIDTH,
    LCD_HEIGHT
)

KEY_R = 114
KEY_1 = 49
KEY_2 = 50

INC = float(1)
PI_ENABLE = True
LCD_ENABLE = True


class Tester(object):

    # UI
    stdscr = None
    scrref = True
    width = 0
    height = 0

    # Controll
    speed = 1
    throttle = float(0)
    reverse = False

    # Sensor
    state_left = False
    state_right = False
    state_enter = False

    hallog = """ """

    # Internal component
    pi_btn_left = None
    pi_btn_right = None
    pi_btn_enter = None
    pi_tacho = None
    pi_revr = None
    pi_spdr = None
    pi_pwm = None
    lcd_device = None

    def stop(self):
        if (self.pi_pwm is not None):
            self.pi_pwm.off()
            self.pi_pwm.value = 0.0
        print("Goodbye !")

    def __init__(self):
        print("Loading...")

        if (LCD_ENABLE):
            self.init_lcd()

        if (PI_ENABLE):
            self.init_pi()

        atexit.register(self.stop)

        curses.wrapper(self.draw_main)

    def init_pi(self):
        from gpiozero import Button, LED, PWMOutputDevice
        from tachometer import Tachometer

        # Input
        self.pi_btn_left = Button(IN_KEY_LEFT)
        self.pi_btn_right = Button(IN_KEY_RIGHT)
        self.pi_btn_enter = Button(IN_KEY_ENTER)

        # Output
        self.pi_revr = LED(OUT_REVERSE)
        self.pi_spdr = LED(OUT_SPD)
        self.pi_pwm = PWMOutputDevice(OUT_THROTTLE)

        self.pi_btn_left.when_pressed = self.btn_left_press
        self.pi_btn_left.when_released = self.btn_left_unpress
        self.pi_btn_right.when_pressed = self.btn_right_press
        self.pi_btn_right.when_released = self.btn_right_unpress
        self.pi_btn_enter.when_pressed = self.btn_enter_press
        self.pi_btn_enter.when_released = self.btn_enter_unpress

        # Tachometer
        self.pi_tacho = Tachometer()

        self.stop()

    def init_lcd(self):
        from luma.core.interface.serial import i2c
        from luma.core.render import canvas
        from luma.oled.device import sh1106

        serial_interface = i2c(port=1, address=LCD_ADDR)
        self.lcd_device = sh1106(serial_interface,
                        width=LCD_WIDTH,
                        height=LCD_HEIGHT,
                        rotate=0)
        self.lcd_device.show()

        with canvas(self.lcd_device) as draw:
            font_size = 20
            name = "OpenWinch tester !"

            x = 0
            y = 0

            draw.rectangle(self.lcd_device.bounding_box, outline="white", fill="black")
            draw.text((10, 25), name, fill="white")

    def btn_left_press(self):
        self.state_left = True
        self.scrref = True

    def btn_left_unpress(self):
        self.state_left = False
        self.scrref = True

    def btn_right_press(self):
        self.state_right = True
        self.scrref = True

    def btn_right_unpress(self):
        self.state_right = False
        self.scrref = True

    def btn_enter_press(self):
        self.state_enter = True
        self.scrref = True

    def btn_enter_unpress(self):
        self.state_enter = False
        self.scrref = True

    def format_title(self, win, pos_x, pos_y, title):
        # win.attron(curses.color_pair(1))
        # win.attron(curses.A_BOLD)
        win.addstr(pos_y, pos_x, title)
        # win.attroff(curses.color_pair(1))
        # win.attroff(curses.A_BOLD)

    def draw_title(self):
        title = "OpenWinch Board Tester"[:self.width-1]
        subtitle = "Written by Mickael Gaillard"[:self.width-1]

        start_x_title = int((self.width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((self.width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)

        # Turning on attributes for title
        # self.stdscr.attron(curses.color_pair(2))
        # self.stdscr.attron(curses.A_BOLD)

        # Rendering title
        self.stdscr.addstr(0, start_x_title, title)

        # Turning off attributes for title
        # self.stdscr.attroff(curses.color_pair(2))
        # self.stdscr.attroff(curses.A_BOLD)

        self.stdscr.addstr(0 + 1, start_x_subtitle, subtitle)

    def draw_statusbar(self):
        statusbarstr = "Press 'q' to exit | STATUS BAR | "

        # Render status bar
        # self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(self.height-1, 1, statusbarstr)
        self.stdscr.addstr(self.height-1, len(statusbarstr),
                           " " * (self.width - len(statusbarstr) - 1))
        # self.stdscr.attroff(curses.color_pair(3))

    def draw_button(self):
        pos_x = 42
        pos_y = 10

        # Title
        self.format_title(self.stdscr, pos_x, pos_y, "Buttons")

        # Value
        pos_xv = pos_x + 1
        self.stdscr.addstr(pos_y + 1,
                           pos_xv,
                           "Left : {}".format(self.state_left))

        self.stdscr.addstr(pos_y + 2,
                           pos_xv,
                           "Enter : {}".format(self.state_enter))

        self.stdscr.addstr(pos_y + 3,
                           pos_xv,
                           "Right : {}".format(self.state_right))

    def draw_info(self):
        pos_x = 19
        pos_y = 10

        # Title
        self.format_title(self.stdscr, pos_x, pos_y, "Stat")

        # Value
        pos_xv = pos_x + 1
        if (self.pi_tacho is not None):
            self.stdscr.addstr(pos_y + 1,
                               pos_xv,
                               "RPM : {}".format(self.pi_tacho.get_rpm()))

            self.stdscr.addstr(pos_y + 2,
                               pos_xv,
                               "K/M : {}".format(self.pi_tacho.get_kph()))

            self.stdscr.addstr(pos_y + 3,
                               pos_xv,
                               "Rotation : {}".format(
                                   self.pi_tacho.get_rotation()))
        else:
            self.stdscr.addstr(pos_y + 1, pos_xv, "RPM : No Tacho !")
            self.stdscr.addstr(pos_y + 2, pos_xv, "K/M : No Tacho !")
            self.stdscr.addstr(pos_y + 3, pos_xv, "Rotation : No Tacho !")

    def draw_hall(self):
        pos_x = 62
        pos_y = 4

        # Title
        self.format_title(
            self.stdscr,
            pos_x,
            pos_y,
            "Hall WVU : {} {} {}".format(1, 2, 3))

        # Windows
        win = self.stdscr.subwin(
            self.height - pos_y - 2,
            self.width - pos_x - 2,
            pos_y + 1,
            pos_x + 1)

        win.addstr(0, 0, self.hallog)

    def draw_speed(self):
        pos_x = 42
        pos_y = 4

        # Title
        self.format_title(
            self.stdscr,
            pos_x,
            pos_y,
            "Speed : {}".format(self.speed))

        # Value
        self.stdscr.addstr(pos_y + 2, pos_x + 4, "1 : Low")
        self.stdscr.addstr(pos_y + 3, pos_x + 4, "2 : High")

        # Windows
        win = self.stdscr.subwin(4, 3, pos_y + 1, pos_x)
        win.border(0)

        # Selector
        win.addstr(self.speed, 1, '█')

    def draw_reverse(self):
        pos_x = 19
        pos_y = 4

        # Title
        self.format_title(
            self.stdscr,
            pos_x,
            pos_y,
            "Reverse : {}".format(self.reverse))

        # Value
        self.stdscr.addstr(pos_y + 2, pos_x + 4, "r : Toggle")

        # Windows
        win = self.stdscr.subwin(3, 3, pos_y + 1, pos_x)
        win.border(0)

        # State
        if (self.reverse):
            win.addstr(1, 1, '█')

    def draw_throttle(self):
        pos_x = 2
        pos_y = 4
        pos_xv = pos_x + 4

        # Title
        self.format_title(
            self.stdscr,
            pos_x,
            pos_y,
            "Throttle {}".format(round(self.throttle, 2)))

        # Value
        self.stdscr.addstr(pos_y + 10, pos_xv, "↑ : Up")
        self.stdscr.addstr(pos_y + 11, pos_xv, "↓ : Down")

        # Windows
        win = self.stdscr.subwin(12, 3, pos_y + 1, pos_x)
        win.border(0)

        # State
        pos = int(self.throttle) + 1
        if pos > 0 and pos <= 11:
            for x in range(1, pos):
                win.addstr(11 - x, 1, '█')

    def draw_main(self, stdscr):
        k = 0

        self.stdscr = stdscr

        curses.noecho()
        stdscr.nodelay(1)

        # Clear and refresh the screen for a blank canvas
        self.stdscr.clear()
        self.stdscr.refresh()

        # Start colors in curses
        # curses.start_color()
        # curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        # curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Loop where k is the last character pressed
        while (k != ord('q')):
            update_throttle = False

            # Throttle
            if k == curses.KEY_DOWN:
                if (self.throttle > 0):
                    self.throttle = self.throttle - INC
                    update_throttle = True
                    self.scrref = True
            elif k == curses.KEY_UP:
                if (self.throttle < 10):
                    self.throttle = self.throttle + INC
                    update_throttle = True
                    self.scrref = True

            # Reverse
            elif k == KEY_R:
                self.reverse = not self.reverse
                if (self.reverse):
                    if (self.pi_revr is not None):
                        self.pi_revr.on()
                    self.scrref = True
                else:
                    if (self.pi_revr is not None):
                        self.pi_revr.off()
                    self.scrref = True

            # Speed
            elif k == KEY_1:
                self.speed = 1
                if (self.pi_spdr is not None):
                    self.pi_spdr.off()
                self.scrref = True
            elif k == KEY_2:
                self.speed = 2
                if (self.pi_spdr is not None):
                    self.pi_spdr.on()
                self.scrref = True

            # Apply Throttle
            if (update_throttle):
                if (self.throttle < 1):
                    if (self.pi_pwm is not None):
                        self.pi_pwm.off()
                        self.pi_pwm.value = 0
                    self.scrref = True
                else:
                    j = self.throttle * 0.1
                    if (self.pi_pwm is not None):
                        self.pi_pwm.on()
                        self.pi_pwm.value = j
                    self.scrref = True

            # Initialization
            if (self.scrref):

                self.stdscr.clear()
                self.height, self.width = self.stdscr.getmaxyx()
                self.stdscr.border()

                self.draw_title()

                self.draw_throttle()
                self.draw_speed()
                self.draw_reverse()
                self.draw_hall()
                self.draw_info()
                self.draw_button()

                self.draw_statusbar()

                # Refresh the screen
                self.stdscr.refresh()
                self.scrref = False

            # Wait for next input
            k = self.stdscr.getch()

            time.sleep(0.2)


if __name__ == "__main__":
    Tester()
