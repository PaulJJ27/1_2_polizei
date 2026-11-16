from gpiozero import LED, PWMLED, DistanceSensor
from time import sleep
from threading import Thread, Event
import pin_config

"""
rear_light = PWMLED(22) 
day_light = PWMLED(23) 
right_blue = PWMLED(17) 
left_blue = PWMLED(27)
break_light = PWMLED(24)
warn_light = PWMLED(5)
turn_right = PWMLED(5)
turn_left = PWMLED(5)
"""

# -------------------------
# rear lights
# -------------------------

def rear_light_on():
    pin_config.rear_light.value = 0.2
    while pin_config.break_light.value == 1:
        pin_config.rear_light.value = 0.7

def rear_light_off():
    pin_config.rear_light.value = 0

# -------------------------
# break light
# -------------------------

def break_light_on():
    pin_config.break_light.value = 1

def break_light_off():
    pin_config.break_light.value = 0

# -------------------------
# day lights
# -------------------------

def day_light_on():
    pin_config.day_light.value = 0.3

def day_light_off():
    pin_config.day_light.value = 0

# -------------------------
# warning lights
# -------------------------

_warn_light_stop = Event()
_warn_light_thread = None

def _warn_light_loop():
    while not _warn_light_stop.is_set():
        pin_config.warn_light.on()
        sleep(0.5)
        pin_config.warn_light.off()
        sleep(0.5)
    pin_config.warn_light.off()

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
        pin_config.blue_left.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        pin_config.blue_right.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        sleep(0.5)
        pin_config.blue_left.blink(on_time=0.1, off_time=0.05, n=2, background=False)
        pin_config.blue_right.blink(on_time=0.1, off_time=0.05, n=2, background=False)
        sleep(0.1)

    pin_config.blue_left.off()
    pin_config.blue_right.off()

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

#sensor = DistanceSensor(echo=24, trigger=23)
green = PWMLED(15)
red = PWMLED(14)
green_time = 0

_parking_stop = Event()
_parking_thread = None

def _parking_loop():
    while not _parking_stop.is_set():
        cm = pin_config.dist_sensor.distance * 100
        #print(cm)
        if cm >= 50:
            red.off()
            green.on()
            sleep(0.5)
            #print("meow")
        elif cm >= 15:
            green.off()
            red.on()
            _parking_stop.wait(cm / 100)
            red.off()
            _parking_stop.wait(cm / 100)
            #print("Hindernis erkannt")
        else:
            green.off()
            red.on()
            _parking_stop.wait(0.3)
            #print("Hindernis erkannt")

def parking_on():

    global _parking_thread
    if _parking_thread and _parking_thread.is_alive():
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
    pin_config.blink_left.off()
    pin_config.blink_left.blink(on_time=0.5, off_time=0.5)

def turn_right_on():
    pin_config.blink_right.off()
    pin_config.blink_right.blink(on_time=0.5, off_time=0.5)

def turn_signal_off():
    pin_config.blink_right.off()
    pin_config.blink_left.off()
            
# -------------------------
# everything off
# -------------------------

def turn_off():
    blue_light_off()
    warn_licht_off()
    rear_light_off()
    break_light_off()
    day_light_off()


if __name__ == "__main__":
    try:
        rear_light_on()
        blue_light_on()
        while True:
            sleep(1)
    except KeyboardInterrupt:
        turn_off()

