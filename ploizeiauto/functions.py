from gpiozero import LED, PWMLED, DistanceSensor, DigitalInputDevice
from time import sleep
from threading import Thread, Event


rear_light = PWMLED(22) 
day_light = PWMLED(23) 
right_blue = PWMLED(17) 
left_blue = PWMLED(27)
break_light = PWMLED(24)
warn_light = PWMLED(5)
turn_right = PWMLED(5)
turn_left = PWMLED(5)


# -------------------------
# rear lights
# -------------------------

def rear_light_on():
    rear_light.value = 0.2
    while break_light.value == 1:        # rear lights will be brighter if you press breaks
        rear_light.value = 0.7

def rear_light_off():
    rear_light.value = 0

# -------------------------
# break light
# -------------------------

def break_light_on():
    break_light.value = 1

def break_light_off():
    break_light.value = 0

# -------------------------
# day lights
# -------------------------

def day_light_on():
    day_light.value = 0.3

def day_light_off():
    day_light.value = 0

# -------------------------
# warning lights
# -------------------------

_warn_light_stop = Event()
_warn_light_thread = None

def _warn_light_loop():
    while not _warn_light_stop.is_set():
        warn_light.on()
        sleep(0.5)
        warn_light.off()
        sleep(0.5)
    warn_light.off()

def warn_light_on():
    global _warn_licht_thread
    if _warn_light_thread and _warn_light_thread.is_alive():
        return

    _warn_light_stop.clear()
    _warn_licht_thread = Thread(target=_warn_light_loop, daemon=True)
    _warn_licht_thread.start()

def warn_licht_off():
    _warn_light_stop.set()

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

def blue_light_off():
    _blue_light_stop.set()

# -------------------------
# parking sensor
# -------------------------

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
    if _parking_stop and _parking_stop.is_alive():
        return
    
    _parking_stop.clear()
    _parking_thread = Thread(target=_parking_loop, daemon=True)
    _parking_thread.start()

def parking_off():
    _parking_stop.set()


# -------------------------
# turn signals left or right
# -------------------------

def turn_left_on():
    turn_right.off()
    turn_right.blink(on_time=0.5, off_time=0.5)

def turn_right_on():
    turn_left.off()
    turn_right.blink(on_time=0.5, off_time=0.5)

def turn_signal_off():
    turn_right.off()
    turn_left.off()

# -------------------------
# headlights 
# -------------------------

light_sensor = DigitalInputDevice(26, pull_up=False)
headlights = LED(5)

# When too dark --> headlights will turn on by themselfes
def headlights_auto_on():

    # when light sensor is deactivated it gives '0' and headlights turn on automatically 
    light_sensor.when_deactivated = headlights.on

    # when light sensor is activated it gives '1' and headlights turn off automatically
    light_sensor.when_activated = headlights.off

    if light_sensor.value == 0:
        headlights.on()
    else:
        headlights.off()

# Function that will be used to turn off auto mode for headlights
def headligths_auto_off():
    light_sensor.when_deactivated = None
    light_sensor.when_activated = None
    headlights.off()

def headlights_on():
    headligths_auto_off()
    headlights.on()

def headlights_off():
    headligths_auto_off()
    headlights.off()

            
# -------------------------
# everything off
# -------------------------

def turn_off():
    blue_light_off()
    warn_licht_off()
    rear_light_off()
    break_light_off()
    day_light_off()
    parking_off()
    headligths_auto_off()
    headlights_off()
