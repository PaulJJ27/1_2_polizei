from gpiozero import LED, PWMLED, DistanceSensor, DigitalInputDevice
from threading import Thread, Event


# =========================================================
# PINS – Platzhalter, später anpassen (jeder Pin nur EINMAL!)
# =========================================================
rear_light          = PWMLED(22)
day_light           = PWMLED(23)
right_blue          = PWMLED(17)
left_blue           = PWMLED(27)
brakes_light        = PWMLED(24)
warn_light          = PWMLED(25)                       # NEU: eigener Pin
turn_right          = PWMLED(5)
turn_left           = PWMLED(6)                        # NEU: eigener Pin
back_driving_lights = PWMLED(13)                       # NEU: eigener Pin
headlights          = LED(19)                          # NEU: eigener Pin
light_sensor        = DigitalInputDevice(26, pull_up=False, bounce_time=0.3)   # NEU: bounce_time
green               = PWMLED(12)                       # NEU: eigener Pin
red                 = PWMLED(16)                       # NEU: eigener Pin
sensor              = DistanceSensor(echo=20, trigger=21)                       # NEU: eigene Pins


# -------------------------
# back driving lights
# -------------------------

def back_driving_lights_on():
    back_driving_lights.value = 1

def back_driving_lights_off():
    back_driving_lights.value = 0


# -------------------------
# rear lights
# -------------------------

_rear_on = False
_brakes = False

def rear_light_on():
    global _rear_on
    _rear_on = True
    _rear_update()

def rear_light_off():
    global _rear_on
    _rear_on = False
    _rear_update()

def _rear_update():                     # rear lights get brighter
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
    global _brakes
    _brakes = False
    brakes_light.value = 0
    _rear_update()


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
        _warn_light_stop.wait(0.5)
        warn_light.off()
        _warn_light_stop.wait(0.5)
    warn_light.off()

def warn_light_on():
    global _warn_light_thread
    if _warn_light_thread and _warn_light_thread.is_alive():
        return
    _warn_light_stop.clear()
    _warn_light_thread = Thread(target=_warn_light_loop, daemon=True)
    _warn_light_thread.start()

def warn_light_off():
    _warn_light_stop.set()
    if _warn_light_thread:                             # NEU
        _warn_light_thread.join(timeout=1)             # NEU


# -------------------------
# blue lights
# -------------------------

_blue_light_stop = Event()
_blue_light_thread = None

def _blink_loop():
    while not _blue_light_stop.is_set():
        left_blue.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        right_blue.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        if _blue_light_stop.wait(0.5):                 # NEU: sofort raus bei Stopp
            break
        left_blue.blink(on_time=0.1, off_time=0.05, n=2, background=False)
        right_blue.blink(on_time=0.1, off_time=0.05, n=2, background=False)
        _blue_light_stop.wait(0.1)

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
    if _blue_light_thread:                             # NEU
        _blue_light_thread.join(timeout=1)             # NEU


# -------------------------
# parking sensor
# -------------------------

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

    green.off()
    red.off()

def parking_on():
    global _parking_thread
    if _parking_thread and _parking_thread.is_alive():
        return
    _parking_stop.clear()
    _parking_thread = Thread(target=_parking_loop, daemon=True)
    _parking_thread.start()

def parking_off():
    _parking_stop.set()
    if _parking_thread:                                # NEU
        _parking_thread.join(timeout=1)                # NEU


# -------------------------
# turn signals left or right
# -------------------------

_turn_left_active = False                              # NEU
_turn_right_active = False                             # NEU

def turn_left_on():
    global _turn_left_active, _turn_right_active       # NEU
    turn_right.off()
    _turn_right_active = False                         # NEU
    turn_left.blink(on_time=0.5, off_time=0.5)
    _turn_left_active = True                           # NEU

def turn_right_on():
    global _turn_left_active, _turn_right_active       # NEU
    turn_left.off()
    _turn_left_active = False                          # NEU
    turn_right.blink(on_time=0.5, off_time=0.5)
    _turn_right_active = True                          # NEU

def turn_signal_off():
    global _turn_left_active, _turn_right_active       # NEU
    turn_right.off()
    turn_left.off()
    _turn_left_active = False                          # NEU
    _turn_right_active = False                         # NEU


# -------------------------
# headlights
# -------------------------

_headlights_auto = False                               # NEU

# When too dark --> headlights will turn on by themselves
def headlights_auto_on():
    global _headlights_auto                            # NEU
    _headlights_auto = True                            # NEU
    light_sensor.when_deactivated = headlights.on      # dark -> on
    light_sensor.when_activated = headlights.off       # bright -> off
    if light_sensor.value == 0:                        # check current state once
        headlights.on()
    else:
        headlights.off()

def headlights_auto_off():
    global _headlights_auto                            # NEU
    _headlights_auto = False                           # NEU
    light_sensor.when_deactivated = None
    light_sensor.when_activated = None
    headlights.off()

def headlights_on():
    headlights_auto_off()
    headlights.on()

def headlights_off():
    headlights_auto_off()


# -------------------------
# status (for Flask: which lights are on?)             # NEU: ganzer Abschnitt
# -------------------------

def is_warn_light_on():
    return _warn_light_thread is not None and _warn_light_thread.is_alive()

def is_blue_light_on():
    return _blue_light_thread is not None and _blue_light_thread.is_alive()

def is_parking_on():
    return _parking_thread is not None and _parking_thread.is_alive()

def is_turn_left_on():
    return _turn_left_active

def is_turn_right_on():
    return _turn_right_active

def is_day_light_on():
    return day_light.value > 0

def is_headlights_on():
    return headlights.is_lit

def is_headlights_auto_on():
    return _headlights_auto

def is_rear_light_on():
    return _rear_on

def is_brakes_light_on():
    return _brakes

def is_back_driving_lights_on():
    return back_driving_lights.value > 0


# -------------------------
# everything off
# -------------------------

def turn_off():
    blue_light_off()
    warn_light_off()
    parking_off()
    headlights_off()
    turn_signal_off()
    rear_light_off()
    brakes_light_off()
    day_light_off()
    back_driving_lights_off()
