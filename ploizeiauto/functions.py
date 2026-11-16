from gpiozero import LED, PWMLED, DistanceSensor, DigitalInputDevice
from time import sleep
from threading import Thread, Event
import config





rear_light = config.rear_lights
day_light = config.day_lights
right_blue = config.blue_right 
left_blue = config.blue_left
break_lights = config.break_light
turn_right = config.blink_right
turn_left = config.blink_left
back_driving_lights = config.reverse_lights
light_sensor = config.day_light_sensor
headlights = config.front_lights

# -------------------------
# back_driving lights
# -------------------------
'''
def back_driving_lights_on():
    back_driving_lights.value = 1

def back_driving_lights_off():
    back_driving_lights.value = 0

'''

# -------------------------
# rear lights
# -------------------------

is_rear_light_on = False

def rear_light_on():
    global is_rear_light_on
    rear_light.value = 0.2
    is_rear_light_on = True
    while break_light_on().break_light.value == 1:        # rear lights will be brighter if you press breaks
        rear_light.value = 0.7
        

def rear_light_off():
    global is_rear_light_on
    rear_light.value = 0
    is_rear_light_on = False

# -------------------------
# break light
# -------------------------

is_brake_light_on = False


def break_light_on():
    global is_brake_light_on
    break_lights.value = 1
    is_brake_light_on = True
    print("Bremslicht an")

def break_light_off():
    global is_brake_light_on
    break_lights.value = 0
    is_brake_light_on = False
    print("Bremslicht aus")

# -------------------------
# day lights
# -------------------------

is_daylight_on = False

def day_light_on():
    global is_daylight_on
    day_light.value = 0.3
    is_daylight_on = True
    print("Tagfahrlicht an")

def day_light_off():
    global is_daylight_on
    day_light.value = 0
    is_daylight_on = False
    print("Tagfahrlicht aus")


# -------------------------
# warning lights
# -------------------------

_warn_light_stop = Event()
_warn_light_thread = None

def _warn_light_loop():
    while not _warn_light_stop.is_set():
        turn_right.on()
        turn_left.on()
        sleep(0.5)
        turn_right.off()
        turn_left.off()
        sleep(0.5)
    turn_right.off()
    turn_left.off()

def warn_light_on():
    global _warn_licht_thread
    if _warn_light_thread and _warn_light_thread.is_alive():
        return

    _warn_light_stop.clear()
    _warn_licht_thread = Thread(target=_warn_light_loop, daemon=True)
    _warn_licht_thread.start()
    print("Warnblinker an")

def warn_licht_off():
    _warn_light_stop.set()
    print("Warnblinker aus")

# -------------------------
# sirene
# -------------------------

_blue_light_stop = Event()
_blue_light_thread = None

def _blink_loop():
    while not _blue_light_stop.is_set():
        left_blue.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        right_blue.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        sleep(0.5)
        left_blue.blink(on_time=0.1, off_time=0.05, n=2, background=False)
        right_blue.blink(on_time=0.1, off_time=0.05, n=2, background=False)
        sleep(0.1)

    left_blue.off()
    right_blue.off()

def blue_light_on():
    global _blue_light_thread
    if _blue_light_thread and _blue_light_thread.is_alive():
        return
    
    _blue_light_stop.clear()
    _blue_light_thread = Thread(target=_blink_loop, daemon=True)
    _blue_light_thread.start()
    print("Blaulicht an")

def blue_light_off():
    _blue_light_stop.set()
    print("Blauclicht aus")
# -------------------------
# parking sensor
# -------------------------
'''
sensor = DistanceSensor(echo=24, trigger=23)
green = PWMLED(27)
red = PWMLED(17)
green_time = 0

_parking_stop = Event()
_parking_thread = None

def _parking_loop():
    while not _parking_stop.is_set():
        cm = sensor.distance * 100

        if cm >= 50:
            red.off()
            green.on()
            _parking_stop.wait(0.2)
        elif cm >= 15:
            green.off()
            red.on()
            _parking_stop.wait(cm / 100)
            red.off()
            _parking_stop.wait(cm / 100)
        else:
            green.off()
            red.on()
            _parking_stop.wait(0.3)
            print("Hindernis erkannt")

def parking_on():

    global _parking_thread
    if _parking_thread and _parking_thread.is_alive():
        return
    
    _parking_stop.clear()
    _parking_thread = Thread(target=_parking_loop, daemon=True)
    _parking_thread.start()

def parking_off():
    _parking_stop.set()


'''    

# -------------------------
# turn signals left or right
# -------------------------

is_turn_left_on = False
is_turn_right_on = False

def turn_left_on():
    global is_turn_left_on
    turn_right.off()
    turn_left.blink(on_time=0.5, off_time=0.5)
    is_turn_left_on = True
    print("Blinker links an")

def turn_right_on():
    global is_turn_right_on
    turn_left.off()
    turn_right.blink(on_time=0.5, off_time=0.5)
    is_turn_right_on = True
    print("Blinker rechts an")

def turn_signal_off():
    global is_turn_left_on
    global is_turn_right_on
    turn_right.off()
    turn_left.off()
    is_turn_left_on = False
    is_turn_right_on = False
    print("Alle Blinker aus")

# -------------------------
# headlights 
# -------------------------


is_headlights_on = False

# When too dark --> headlights will turn on by themselfes
def headlights_auto_on():
    global is_headlights_on

    # when light sensor is deactivated it gives '0' and headlights turn on automatically 
    light_sensor.when_deactivated = headlights.on
    is_headlights_on = True

    # when light sensor is activated it gives '1' and headlights turn off automatically
    light_sensor.when_activated = headlights.off
    is_headlights_on = False
    
    # it will check if its already dark or bright (needed for the first check)
    if light_sensor.value == 0:
        headlights.on()
        is_headlights_on = True
    else:
        headlights.off()
        is_headlights_on = False

# Function that will be used to turn off auto mode for headlights
def headligths_auto_off():
    global is_headlights_on
    light_sensor.when_deactivated = None
    light_sensor.when_activated = None
    headlights.off()
    is_headlights_on = False


def headlights_on():
    global is_headlights_on
    headligths_auto_off()
    headlights.on()
    is_headlights_on = True
    print("Scheinwerfer an")

def headlights_off():
    global is_headlights_on
    headligths_auto_off()
    headlights.off()
    is_headlights_on = False
    print("Scheinwerfer aus")

            
# -------------------------
# everything off
# -------------------------

def turn_off():
    global is_rear_light_on
    global is_brake_light_on
    global is_daylight_on
    global is_turn_left_on
    global is_turn_right_on
    global is_headlights_on


    blue_light_off()
    warn_licht_off()
    rear_light_off()
    break_light_off()
    day_light_off()
    #parking_off()
    headligths_auto_off()
    headlights_off()
    is_rear_light_on = False
    is_brake_light_on = False
    is_daylight_on = False
    is_turn_left_on = False
    is_turn_right_on = False
    is_headlights_on = False


---------------------
_rear_on = False
_brakes = False

def rear_light_on():
    global _rear_on
    _rear_on = True
    _rear_update()
    
def rear_light_off():
    rear_light.value = 0

def _rear_update():                     # It will be possible to make rear lights brighter
    if not _rear_on:                    # when brakes are pressed
        rear_light.value = 0
    elif _brakes:
        rear_light.value = 1
    else:
        rear_light.value = 0.6
        
# -------------------------
# brakes light
# -------------------------

def brakes_light_on():
    global _brakes
    _brakes = True
    brakes_light.value = 1
    _rear_update()

def brakes_light_off():
    brakes_light.value = 0
