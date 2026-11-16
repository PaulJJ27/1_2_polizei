from gpiozero import PWMLED, LED, DistanceSensor, Buzzer, DigitalInputDevice

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
day_light_sensor = DigitalInputDevice(22, pull_up=False)

dist_sensor = DistanceSensor(echo=6, trigger=5)

