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


def siren_sound():
    for n in range(700,900,200):
        pwm.ChangeFrequency(n)
        sleep(0.4)
    for n in range(900, 700, -200):
        pwm.ChangeFrequency(n)
        sleep(0.4)





