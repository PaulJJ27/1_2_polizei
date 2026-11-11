from gpiozero import LED, PWMLED, DistanceSensor
from time import sleep
from threading import Thread, Event


rear_light = PWMLED(22) 
day_light = PWMLED(23) 
right_blue = PWMLED(17) 
left_blue = PWMLED(27)
break_light = PWMLED(24)
warn_light = PWMLED(5)


# -------------------------
# rear lights
# -------------------------

def rear_light_on():
    rear_light.value = 0.2

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

def parking():

    while True:

        if sensor.distance * 100 >= 51:
            red.value = 0
            green.value = 1
            green_time += 1
            print("Bereich seit ", green_time, " Sekunden frei")
        elif sensor.distance * 100 > 15 and sensor.distance * 100 < 51:
            red.value = 0
            green.value = 0
            red.blink(on_time=sensor.distance, off_time=sensor.distance)
            green_time = 0
            print("Hindernis erkannt")
        else:
            red.value = 1
            green.value = 0
            green_time = 0
            print("Hindernis erkannt")
            
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
