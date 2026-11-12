from gpiozero import PWMLED, LED, DistanceSensor, Buzzer
from time import sleep
import mfrc522
import RPi.GPIO as GPIO
import signal

GPIO.setwarnings(False)

buzzer = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

pwm = GPIO.PWM(buzzer, 700)
pwm.start(50)


#def siren_sound():
try:
    while True:
        for n in range(700,900,200):
            pwm.ChangeFrequency(n)
            sleep(0.4)
        for n in range(900, 700, -200):
            pwm.ChangeFrequency(n)
            sleep(0.4)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()





status = None
reader = mfrc522.MFRC522()
corr = [122, 231, 109, 127, 143]

def key_check():
    try:
        print("Hold tag near the reader")
        while True:
            status, tag_type = reader.Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                status, uid = reader.Anticoll()
                if status == reader.MI_OK:
                    #print(uid)
                    break
            sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

    if uid == corr:
        return "unlock"




