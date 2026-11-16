from gpiozero import PWMLED, LED, DistanceSensor, Buzzer, LightSensor

buzzer = 21

day_light = PWMLED(20)
front_lights = PWMLED(16)
blue_left = PWMLED(26)
blue_right = PWMLED(19)
blink_left = PWMLED(24)
blink_right = PWMLED(23)
break_light = PWMLED(13)
rear_light = PWMLED(12)
reverse_light = PWMLED(27)

light_sensor = LightSensor(22)

dist_sensor = DistanceSensor(echo=6, trigger=5)

