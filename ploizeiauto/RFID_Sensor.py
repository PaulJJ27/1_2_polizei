from time import sleep
import mfrc522
import RPi.GPIO as GPIO

rfid_reader = mfrc522.MFRC522()

status = None

corr = [122, 231, 109, 127, 143]

is_unlocked = False

def key_check():
        global is_unlocked
        print("Hold tag near the reader")
        while True:
            status, tag_type = rfid_reader.Request(rfid_reader.PICC_REQIDL)
            if status == rfid_reader.MI_OK:
                status, uid = rfid_reader.Anticoll()
                if status == rfid_reader.MI_OK:
                    #print(uid)
                    break
            sleep(0.2)
        if uid == corr:
            print("unlock")
            is_unlocked = True
        else:
            is_unlocked = False
            print("lock")
    

        GPIO.cleanup()


while True:
    key_check()
    sleep(1)