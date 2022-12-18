'''

TRIANGLE CODE

import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep


GPIO.setmode(GPIO.BOARD)             # choose BCM or BOARD
GPIO.setup(21, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)# set GPIO24 as an output
GPIO.setwarnings(False)

def fwrd(t):
    GPIO.output(13,1)
    GPIO.output(21, 1)
    sleep(t)
    GPIO.output(21, 0)
    GPIO.output(13, 0)

def bkwrd(t):
    GPIO.output(23,1)
    GPIO.output(15, 1)
    sleep(t)
    GPIO.output(23, 0)
    GPIO.output(15, 0)

def rght(t):
    GPIO.output(13,1)
    GPIO.output(23, 1)
    sleep(t)
    GPIO.output(13, 0)
    GPIO.output(23, 0)

def lft(t):
    GPIO.output(21,1)
    GPIO.output(15, 1)
    sleep(t)
    GPIO.output(21, 0)
    GPIO.output(15, 0)

def Tri():
    fwrd(0.5)
    lft(0.5)
    fwrd(0.5)
    rght(0.77)
    fwrd(0.5)
    lft(0.5)


#21 =>right foward
#23 =>right backward
#13 =>left foward
#15 =>left Backward
try:
    Tri()

except KeyboardInterrupt:
    GPIO.output(21, 0)
    GPIO.output(13, 0)# trap a CTRL+C keyboard interrupt
    GPIO.cleanup()

    ***************************************
'''
'''
   ***************************************
KEYBOARD CONTROLED WASD USED
NOTE -ONLY USE COMMAND LINE    
'''
import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep
import tty, sys, termios
import select

def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)

def getch(timeout=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setup_term(fd)
        try:
            rw, wl, xl = select.select([fd], [], [], timeout)
        except select.error:
            return
        if rw:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



#from msvcrt import getch             # lets us have a delay
GPIO.setmode(GPIO.BOARD)             # choose BCM or BOARD
GPIO.setup(21, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)# set GPIO24 as an output
GPIO.setwarnings(False)

def fwrd(t):
    GPIO.output(13,1)
    GPIO.output(21, 1)
    sleep(t)
    GPIO.output(21, 0)
    GPIO.output(13, 0)

def bkwrd(t):
    GPIO.output(23,1)
    GPIO.output(15, 1)
    sleep(t)
    GPIO.output(23, 0)
    GPIO.output(15, 0)

def rght(t):
    GPIO.output(13,1)
    GPIO.output(23, 1)
    sleep(t)
    GPIO.output(13, 0)
    GPIO.output(23, 0)

def lft(t):
    GPIO.output(21,1)
    GPIO.output(15, 1)
    sleep(t)
    GPIO.output(21, 0)
    GPIO.output(15, 0)


#21 =>right foward
#23 =>right backward
#13 =>left foward
#15 =>left Backward
try:
    while True:
        key = ord(getch())
        if key == 119:
            fwrd(0.02)#ESC
            #break
        elif key == 100: #Enter
            rght(0.02)
        elif key == 97: #Special keys (arrows, f keys, ins, del, etc.)
            lft(0.02)
        elif key==115:
            bkwrd(0.02)


except KeyboardInterrupt:
    GPIO.output(21, 0)
    GPIO.output(13, 0)# trap a CTRL+C keyboard interrupt
    GPIO.cleanup()


