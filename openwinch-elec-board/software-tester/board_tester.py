import time
import atexit
import curses
from gpiozero import Button, LED, PWMOutputDevice

from hardware_config import OUT_REVERSE, OUT_SPD, OUT_THROTTLE
from constantes import MOTOR_PPR, WINCH_DIAM

KEY_R = 114
KEY_1 = 49
KEY_2 = 50


class Tester(object):

    stdscr = None
    width = 0
    height = 0

    # Controll
    revr = LED(OUT_REVERSE)
    spdr = LED(OUT_SPD)
    pwm = PWMOutputDevice(OUT_THROTTLE)

    speed = 1
    throttle = float(0)
    throttle_inc = float(1)
    reverse = False

    # Sensor
    hsw = Button(23)
    hsv = Button(24)
    hsu = Button(4)

    hallog = """ """
    hsw_count = 0
    hsv_count = 0
    hsu_count = 0

    rpm = 0
    kpm = 0
    rot = False

    rpm_start = 0
    rpm_end = 0

    def stop(self):
        self.pwm.off()
        self.pwm.value = 0

    def __init__(self):
        atexit.register(self.stop)
        curses.wrapper(self.draw_main)

        self.hsw.when_pressed = self.hallW
        self.hsv.when_pressed = self.hallV
        self.hsu.when_pressed = self.hallU

        self.stop()

    iw = 0
    rr = 1
    def hallW(self):
        self.iw = self.iw + self.rr
        self.hsw_count = self.hsw_count + 1
        self.get_rpm()
        self.get_kpm()
        print("W Up! " + str(self.iw))

    iv = 0
    def hallV(self):
        if (self.iv < self.iw):
            self.rr = 1
        else:
            self.rr = -1
        self.iv = self.iv + self.rr
        print("V up! " + str(self.iv))

    iu = 0
    def hallU(self):
        self.iu = self.iu + self.rr
        print("U up! " + str(self.iu))

    def get_kpm(self):
        self.kpm = WINCH_DIAM * self.rpm * 0.1885

    def get_rpm(self):
        self.rpm_end = time.time()

        delta = self.rpm_end - self.rpm_start
        delta = delta / 60
        self.rpm = (self.hsw_count / delta) / MOTOR_PPR

        self.rpm_start = time.time()

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

    def draw_info(self):
        pos_x = 19
        pos_y = 10

        # Title
        self.format_title(self.stdscr, pos_x, pos_y, "Stat")

        # Value
        pos_xv = pos_x + 1
        self.stdscr.addstr(pos_y + 1, pos_xv, "RPM : {}".format(self.rpm))
        self.stdscr.addstr(pos_y + 2, pos_xv, "K/M : {}".format(self.kpm))
        self.stdscr.addstr(pos_y + 3, pos_xv, "Rotation : {}".format(self.rot))

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
        self.stdscr.addstr(pos_y + 9, pos_xv, "↑ : Up")
        self.stdscr.addstr(pos_y + 10, pos_xv, "↓ : Down")

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

            # Initialization
            self.stdscr.clear()
            self.height, self.width = self.stdscr.getmaxyx()
            self.stdscr.border()

            tt = False
            if k == curses.KEY_DOWN:
                if (self.throttle > 0):
                    self.throttle = self.throttle - self.throttle_inc
                    tt = True
            elif k == curses.KEY_UP:
                if (self.throttle < 10):
                    self.throttle = self.throttle + self.throttle_inc
                    tt = True

            # elif k == curses.KEY_RIGHT:
            #     cursor_x = cursor_x + 1
            # elif k == curses.KEY_LEFT:
            #     cursor_x = cursor_x - 1

            elif k == KEY_R:
                self.reverse = not self.reverse
                if (self.reverse):
                    self.revr.on()
                else:
                    self.revr.off()

            elif k == KEY_1:
                self.speed = 1
                self.spdr.off()
            elif k == KEY_2:
                self.speed = 2
                self.spdr.on()

            if (tt):
                if (self.throttle < 1):
                    self.pwm.off()
                    self.pwm.value = 0
                else:
                    j = self.throttle * 0.1
                    self.pwm.on()
                    self.pwm.value = j

            self.draw_title()

            self.draw_throttle()
            self.draw_speed()
            self.draw_reverse()
            self.draw_hall()
            self.draw_info()

            self.draw_statusbar()

            # Refresh the screen
            self.stdscr.refresh()

            # Wait for next input
            k = self.stdscr.getch()


if __name__ == "__main__":
    Tester()
