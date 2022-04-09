import spidev
import os
import uinput
import time
import RPi.GPIO as GPIO
import subprocess
import signal, sys

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000

def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

swt_channel = 0
vrx_channel = 1
vry_channel = 2

swt_channel1 = 3
vrx_channel1 = 4
vry_channel1 = 5


 
# Read switch state
swt_val = ReadChannel(swt_channel)

def signal_handler(signal, frame):
        print ('Grattis, vi ses')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'


GPIO.setmode(GPIO.BCM)
GPIO.setup(0, GPIO.IN, pull_up_down=GPIO.PUD_UP) #A
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) #B
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP) #X
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Y

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #DPADUP
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #DPADDOWN
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) #DPADLEFT
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) #DPADRIGHT

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #L1
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #L2
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #R1
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #R2

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) #START
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) #SELECT
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #HOME

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) #L3
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #R3



#subprocess.call(["sudo", "shutdown", "-h","now"])



device = uinput.Device([uinput.KEY_UP,uinput.KEY_DOWN,uinput.KEY_LEFT,uinput.KEY_RIGHT,
                        uinput.KEY_X, uinput.KEY_ENTER,uinput.KEY_J,uinput.KEY_K, uinput.KEY_L,
                        uinput.KEY_P, uinput.KEY_G, uinput.KEY_Z, uinput.KEY_Q, uinput.KEY_H, 
                        uinput.KEY_I, uinput.KEY_O, uinput.KEY_Y,uinput.KEY_M,
                        uinput.KEY_A, uinput.KEY_B,uinput.KEY_C, uinput.KEY_V, uinput.KEY_N, 
                        uinput.KEY_W, uinput.KEY_S, uinput.KEY_D, uinput.KEY_F, uinput.ABS_X, uinput.ABS_Y])

#Knappar
A = False
B = False
X = False
Y = False
DPADUP = False
DPADDOWN = False
DPADLEFT = False
DPADRIGHT = False

L1 = False
L2 = False
L3 = False
R1 = False 
R2 = False
R3 = False

start = False
select = False
home = False

#Main JS
js0x = 0
js0y = 0

js0xs = True
js0ys = True
js0ysu = True
js0xsu = True


adc_y_up = False
adc_y_down = False

adc_x_up = False
adc_x_down = False

#c-stick
js0x1 = 0
js0y1 = 0

js0xs1 = True
js0ys1 = True
js0ysu1 = True
js0xsu1 = True


adc_y_up1 = False
adc_y_down1 = False

adc_x_up1 = False
adc_x_down1 = False

while True:
    
  # Read the joystick position data
  vrx_pos = ReadChannel(vrx_channel)
  vry_pos = ReadChannel(vry_channel)
  vrx_pos1 = ReadChannel(vrx_channel1)
  vry_pos1 = ReadChannel(vry_channel1)

  if 300 <= vrx_pos <= 700:
   adc_x_up = False
   adc_x_down = False 
  elif vrx_pos > 700:
   adc_x_up = True
   adc_x_down = False
  elif vrx_pos < 300:
   adc_x_up = False
   adc_x_down = True

  if 300 <= vry_pos <= 700:
   adc_y_up = False
   adc_y_down = False
  elif vry_pos > 700:
   adc_y_up = True
   adc_y_down = False
  elif vry_pos <= 300:
   adc_y_up = False
   adc_y_down = True   
    
  #C-stick
  if 300 <= vrx_pos1 <= 700:
   adc_x_up1 = False
   adc_x_down1 = False 
  elif vrx_pos1 > 700:
   adc_x_up1 = True
   adc_x_down1 = False
  elif vrx_pos1 < 300:
   adc_x_up1 = False
   adc_x_down1 = True

  if 300 <= vry_pos1 <= 700:
   adc_y_up1 = False
   adc_y_down1 = False
  elif vry_pos1 > 700:
   adc_y_up1 = True
   adc_y_down1 = False
  elif vry_pos1 <= 300:
   adc_y_up1 = False
   adc_y_down1 = True     



  #if js0y != adc_y:
   #device.emit(uinput.ABS_Y, int(adc_y))
   #js0y = adc_y





  if (not js0ys) and adc_y_up:  # Fire button pressed
    js0ys = True
    #print("js0 y up")
    device.emit(uinput.KEY_DOWN, 1) # Press Left Ctrl key
  elif js0ys and (not adc_y_up):  # Fire button released
    js0ys = False
    device.emit(uinput.KEY_DOWN, 0) # Release Left Ctrl key
    #print("js0 y up release")
  elif (not js0y) and adc_y_down:  # Fire button pressed
    js0y = True
    #print("js0 y down")
    device.emit(uinput.KEY_UP, 1) # Press Left Ctrl key
  elif js0y and (not adc_y_down):  # Fire button released
    js0y = False
    device.emit(uinput.KEY_UP, 0) # Release Left Ctrl key
    #print("js0 y down release")


  if (not js0xs) and adc_x_up:  # Fire button pressed
    js0xs = True
    #print("js0 x right")
    device.emit(uinput.KEY_RIGHT, 1) # Press Left Ctrl key
  elif js0xs and (not adc_x_up):  # Fire button released
    js0xs = False
    device.emit(uinput.KEY_RIGHT, 0) # Release Left Ctrl key
    #print("js0 x right release")
  elif (not js0x) and adc_x_down:  # Fire button pressed
    js0x = True
    #print("js0 x left")
    device.emit(uinput.KEY_LEFT, 1) # Press Left Ctrl key
  elif js0x and (not adc_x_down):  # Fire button released
    js0x = False
    device.emit(uinput.KEY_LEFT, 0) # Release Left Ctrl key
    #print("js0 x left release")

  #C-stick  
  if (not js0ys1) and adc_y_up1:  # Fire button pressed
    js0ys1 = True
    #print("js0 y up")
    device.emit(uinput.KEY_W, 1) # Press Left Ctrl key
  elif js0ys1 and (not adc_y_up1):  # Fire button released
    js0ys1 = False
    device.emit(uinput.KEY_W, 0) # Release Left Ctrl key
    #print("js0 y up release")
  elif (not js0y1) and adc_y_down1:  # Fire button pressed
    js0y1 = True
    #print("js0 y down")
    device.emit(uinput.KEY_S, 1) # Press Left Ctrl key
  elif js0y1 and (not adc_y_down1):  # Fire button released
    js0y1 = False
    device.emit(uinput.KEY_S, 0) # Release Left Ctrl key
    #print("js0 y down release")


  if (not js0xs1) and adc_x_up1:  # Fire button pressed
    js0xs1 = True
    #print("js0 x right")
    device.emit(uinput.KEY_F, 1) # Press Left Ctrl key
  elif js0xs1 and (not adc_x_up1):  # Fire button released
    js0xs1 = False
    device.emit(uinput.KEY_F, 0) # Release Left Ctrl key
    #print("js0 x right release")
  elif (not js0x1) and adc_x_down1:  # Fire button pressed
    js0x1 = True
    #print("js0 x left")
    device.emit(uinput.KEY_D, 1) # Press Left Ctrl key
  elif js0x1 and (not adc_x_down1):  # Fire button released
    js0x1 = False
    device.emit(uinput.KEY_D, 0) # Release Left Ctrl key
    #print("js0 x left release")





  if (not A) and (not GPIO.input(0)):  # A button pressed
    A = True
    #print("A pressed")
    device.emit(uinput.KEY_Enter, 1) # Press Left Ctrl key
  if A and GPIO.input(0):  # A button released
    A = False
    device.emit(uinput.KEY_Enter, 0) # Release Left Ctrl key


  if (not B) and (not GPIO.input(20)):  # B button pressed
    B = True
    #print("B pressed")
    device.emit(uinput.KEY_B, 1) # Press B key
  if B and GPIO.input(20):  # B button released
    B = False
    device.emit(uinput.KEY_B, 0) # Release B key


  if (not X) and (not GPIO.input(14)):  # X button pressed
    X = True
    #print("X pressed")
    device.emit(uinput.KEY_X, 1) # Press X key
  if X and GPIO.input(14):  # X button released
    X = False
    device.emit(uinput.KEY_X, 0) # Release X key


  if (not Y) and (not GPIO.input(15)):  # Y button pressed
    Y = True
    #print("Y pressed")
    device.emit(uinput.KEY_Y, 1) # Press Y key
  if Y and GPIO.input(15):  # Y button released
    Y = False
    device.emit(uinput.KEY_Y, 0) # Release Y key

  if (not DPADUP) and (not GPIO.input(17)):  # Left button pressed
    DPADUP = True
    #print("DPADUP pressed")
    device.emit(uinput.KEY_K, 1) # Press Left key
  if DPADUP and GPIO.input(17):  # Left button released
    DPADUP = False
    device.emit(uinput.KEY_K, 0) # Release Left key


  if (not DPADDOWN) and (not GPIO.input(18)):  # Left button pressed
    DPADDOWN = True
    #print("start pressed")
    device.emit(uinput.KEY_J, 1) # Press Left key
  if DPADDOWN and GPIO.input(18):  # Left button released
    DPADDOWN = False
    device.emit(uinput.KEY_J, 0) # Release Left key

  if (not DPADLEFT) and (not GPIO.input(27)):  # Left button pressed
    DPADLEFT = True
    #print("touch pressed")
    device.emit(uinput.KEY_H, 1) # Press Left key
  if DPADLEFT and GPIO.input(27):  # Left button released
    DPADLEFT = False
    device.emit(uinput.KEY_H, 0) # Release Left key

  if (not DPADRIGHT) and (not GPIO.input(22)):  # Left button pressed
    DPADRIGHT = True
    #print("lsb pressed")
    device.emit(uinput.KEY_I, 1) # Press Left key
  if DPADRIGHT and GPIO.input(22):  # Left button released
    DPADRIGHT = False
    device.emit(uinput.KEY_I, 0) # Release Left key

  if (not L1) and (not GPIO.input(23)):  # Left button pressed
    L1 = True
    #print("rsb pressed")
    device.emit(uinput.KEY_O, 1) # Press Left key
  if L1 and GPIO.input(23):  # Left button released
    L1 = False
    device.emit(uinput.KEY_O, 0) # Release Left key

  if (not L2) and (not GPIO.input(26)):  # Left button pressed
    L2 = True
    #print("select pressed")
    device.emit(uinput.KEY_M, 1) # Press Left key
  if L2 and GPIO.input(26):  # Left button released
    L2 = False
    device.emit(uinput.KEY_M, 0) # Release Left key
 
  if (not L3) and (not GPIO.input(12)):  # Left button pressed
    L3 = True
    #print("select pressed")
    device.emit(uinput.KEY_C, 1) # Press Left key
  if L3 and GPIO.input(12):  # Left button released
    L3 = False
    device.emit(uinput.KEY_C, 0) # Release Left key
    
  if (not R1) and (not GPIO.input(19)):  # Left button pressed
    R1 = True
    #print("select pressed")
    device.emit(uinput.KEY_V, 1) # Press Left key
  if R1 and GPIO.input(19):  # Left button released
    R1 = False
    device.emit(uinput.KEY_V, 0) # Release Left key
    
  if (not R2) and (not GPIO.input(21)):  # Left button pressed
    R2 = True
    #print("select pressed")
    device.emit(uinput.KEY_N, 1) # Press Left key
  if R2 and GPIO.input(21):  # Left button released
    R2 = False
    device.emit(uinput.KEY_N, 0) # Release Left key
    
  if (not R3) and (not GPIO.input(13)):  # Left button pressed
    R3 = True
    #print("select pressed")
    device.emit(uinput.KEY_Q, 1) # Press Left key
  if R3 and GPIO.input(13):  # Left button released
    R3 = False
    device.emit(uinput.KEY_Q, 0) # Release Left key
    
  if (not start) and (not GPIO.input(5)):  # Left button pressed
    start = True
    #print("select pressed")
    device.emit(uinput.KEY_Z, 1) # Press Left key
  if start and GPIO.input(5):  # Left button released
    start = False
    device.emit(uinput.KEY_Z, 0) # Release Left key
    
  if (not select) and (not GPIO.input(6)):  # Left button pressed
    select = True
    #print("select pressed")
    device.emit(uinput.KEY_G, 1) # Press Left key
  if select and GPIO.input(6):  # Left button released
    select = False
    device.emit(uinput.KEY_G, 0) # Release Left key
    
  if (not home) and (not GPIO.input(25)):  # Left button pressed
    home = True
    #print("select pressed")
    device.emit(uinput.KEY_P, 1) # Press Left key
  if home and GPIO.input(24):  # Left button released
    home = False
    device.emit(uinput.KEY_P, 0) # Release Left key
    
  time.sleep(.04)
