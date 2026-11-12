from gpiozero import PWMLED, LED, DistanceSensor, Buzzer
import mfrc522

buzzer = 21

day_lights = PWMLED(20)
front_lights = PWMLED(16)
blue_left = PWMLED(26)
blue_right = PWMLED(19)
blink_left = PWMLED(24)
blink_right = PWMLED(23)
break_light = PWMLED(13)
rear_lights = PWMLED(12)
reverse_lights = PWMLED(7)

dist_sensor = DistanceSensor(Echo=6, trigger=5)

reader = mfrc522.MFRC522()