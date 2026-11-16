from time import sleep
import mfrc522
import RPi.GPIO as GPIO

rfid_reader = mfrc522.MFRC522()

status = None

corr = [122, 231, 109, 127, 143]

def key_check():
    try:
        print("Hold tag near the reader")
        while True:
            status, tag_type = rfid_reader.Request(rfid_reader.PICC_REQIDL)
            if status == rfid_reader.MI_OK:
                status, uid = rfid_reader.Anticoll()
                if status == rfid_reader.MI_OK:
                    #print(uid)
                    break
            sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

    if uid == corr:
        print("unlock")

while True:
    key_check()
    sleep(1)