from time import sleep
from threading import Thread
import mfrc522

rfid_reader = mfrc522.MFRC522()
corr = [122, 231, 109, 127, 143]
is_unlocked = False
_on_change = None

def key_check():
    global is_unlocked
    status, tag_type = rfid_reader.Request(rfid_reader.PICC_REQIDL)
    if status != rfid_reader.MI_OK:
        return
    status, uid = rfid_reader.Anticoll()
    if status != rfid_reader.MI_OK:
        return
    new_state = (uid == corr)
    changed = new_state != is_unlocked
    is_unlocked = new_state
    print("unlock" if is_unlocked else "lock")
    if changed and _on_change:
        _on_change(new_state)

def _reader_loop():
    while True:
        key_check()
        sleep(0.2)

def start_reader(on_change=None):
    global _on_change
    _on_change = on_change
    Thread(target=_reader_loop, daemon=True).start()