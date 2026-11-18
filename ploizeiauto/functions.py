from gpiozero import LED, PWMLED, DistanceSensor, DigitalInputDevice, PWMOutputDevice
from threading import Thread, Event
import RFID_Sensor


rear_light = PWMLED(12)
day_light = PWMLED(20)
right_blue = PWMLED(19)
left_blue = PWMLED(26)
brakes_light = PWMLED(13)
turn_right = PWMLED(23)
turn_left = PWMLED(24)
back_driving_lights = PWMLED(27)
headlights = LED(16)

light_sensor = DigitalInputDevice(22, pull_up=False)
dist_sensor = DistanceSensor(echo=6, trigger=5)
buzzer = PWMOutputDevice(21, frequency=700, initial_value=0)
siren = buzzer
peeep = buzzer(frequency=400)


# -------------------------
# reverse lights
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
        turn_left.on()
        turn_right.on()
        _warn_light_stop.wait(0.5)
        turn_left.off()
        turn_right.off()
        _warn_light_stop.wait(0.5)
    turn_left.off()
    turn_right.off()

def warn_light_on():
    global _warn_light_thread
    if _warn_light_thread and _warn_light_thread.is_alive():
        return

    _warn_light_stop.clear()
    _warn_light_thread = Thread(target=_warn_light_loop, daemon=True)
    _warn_light_thread.start()

def warn_light_off():
    _warn_light_stop.set()

# -------------------------
# blue lights
# -------------------------

_blue_light_stop = Event()
_blue_light_thread = None

def _blink_loop():
    while not _blue_light_stop.is_set():
        left_blue.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        right_blue.blink(on_time=0.1, off_time=0.05, n=2, background=True)
        _blue_light_stop.wait(0.5)
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

# -------------------------
# parking sensor
# -------------------------

_parking_stop = Event()
_parking_thread = None

def _parking_loop():
    while not _parking_stop.is_set():
        cm = dist_sensor.distance * 100

        if cm <= 50 and cm >= 15:
            peeep.value = 1
            _parking_stop.wait(cm / 100)
            peeep.value = 0
            _parking_stop.wait(cm / 100)
        elif cm < 15: 
            peeep.value = 1
            _parking_stop.wait(0.3)

    peeep.value = 0

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

_turn_left_active = False
_turn_right_active = False

def turn_left_on():
    global _turn_left_active, _turn_right_active
    turn_right.off()
    _turn_right_active = False
    turn_left.blink(on_time=0.5, off_time=0.5)
    _turn_left_active = True

def turn_right_on():
    global _turn_left_active, _turn_right_active
    turn_left.off()
    _turn_left_active = False
    turn_right.blink(on_time=0.5, off_time=0.5)
    _turn_right_active = True

def turn_signal_off():
    global _turn_left_active, _turn_right_active
    turn_right.off()
    turn_left.off()
    _turn_left_active = False
    _turn_right_active = False

# -------------------------
# headlights 
# -------------------------

_headlights_auto = False

# When too dark --> headlights will turn on by themselfes
def headlights_auto_on():
    global _headlights_auto
    _headlights_auto = True

    # when light sensor is deactivated it gives '0' and headlights turn on automatically 
    light_sensor.when_deactivated = headlights.on

    # when light sensor is activated it gives '1' and headlights turn off automatically
    light_sensor.when_activated = headlights.off
    
    # it will check if its already dark or bright (needed for the first check)
    if light_sensor.value == 0:
        headlights.on()
    else:
        headlights.off()

# Function that will be used to turn off auto mode for headlights
def headlights_auto_off():
    global _headlights_auto
    _headlights_auto = True
    light_sensor.when_deactivated = None
    light_sensor.when_activated = None
    headlights.off()

def headlights_on():
    headlights_auto_off()
    headlights.on()

def headlights_off():
    headlights_auto_off()
    headlights.off()

# -------------------------
# siren loop  
# -------------------------

_siren_thread = None
_siren_stop = Event()

tones = list(range(700, 900, 50)) + list(range(900, 700, -50)) # Tones: 700->750->800..900->850..

def _siren_loop():
    while not _siren_stop.is_set():
        for n in tones:
            siren.frequency = n
            if _siren_stop.wait(0.1):
                break

def siren_on():
    global _siren_thread
    if _siren_thread and _siren_thread.is_alive():
        return
    
    _siren_thread.clear()
    _siren_thread = Thread(target=_siren_loop, daemon=True)
    _siren_thread.start()

def siren_off():
    _siren_stop.set()
      
# -------------------------
# everything off
# -------------------------

def turn_off():
    blue_light_off()
    warn_light_off()
    rear_light_off()
    brakes_light_off()
    day_light_off()
    parking_off()
    headlights_auto_off()
    headlights_off()
    turn_signal_off()
    back_driving_lights_off()

# -------------------------
# Functions for Flask to chech if it's turned on or turned off
# -------------------------

def get_status():
    return {
        "warnblink_activated":        _warn_light_thread is not None and _warn_light_thread.is_alive(),
        "blinker_links_activated":    _turn_left_active,
        "blinker_rechts_activated":   _turn_right_active,
        "blaulicht_activated":        _blue_light_thread is not None and _blue_light_thread.is_alive(),
        "tagfahrlicht_activated":     day_light.is_lit,
        "scheinwerfer_activated":     headlights.is_lit,
        "scheinwerfer_auto":          _headlights_auto,
        "parksensor_activated":       _parking_thread is not None and _parking_thread.is_alive(),
        "rueklicht_activated":        _rear_on,
        "policecar_locked":           RFID_Sensor.is_unlocked == False,
        "siren_activated":            _siren_thread is not None and _siren_thread.is_alive()
    }
      