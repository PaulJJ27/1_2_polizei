from flask import Flask, render_template, redirect, url_for, request
import functions
from jinja2 import Environment
import RFID_Sensor
#import temp_functions

app = Flask(__name__)

def _lock_changed(unlocked):
    if unlocked:
        functions.day_light_on()
        functions.rear_light_on()
        functions.headlights_auto_on()
    else:
        functions.turn_off()

RFID_Sensor.start_reader(_lock_changed)

@app.before_request
def require_unlock():
    if request.endpoint == "static":
        return
    if not RFID_Sensor.is_unlocked and request.method == "POST":
        return "", 403

@app.post("/brakelight/an")
def brake_light_on():
    print("POST empfangen: brakelight an")
    functions.brakes_light_on()
    return "", 204

@app.post("/brakelight/off")
def brake_light_off():
    print("POST empfangen: brakelight off")
    functions.brakes_light_off()
    return "", 204


@app.route('/', methods=["GET", "POST"])
def control():

    if request.method == "POST":
        form = request.form
        print("POST empfangen:", list(form.keys()))

        if "warnblink" in form:
            functions.warn_light_on()

        elif "warnblink_off" in form:
            functions.warn_licht_off()

        elif "blinker_links" in form:
            functions.turn_left_on()

        elif "blinker_links_off" in form:
            functions.turn_signal_off()

        elif "blinker_rechts" in form:
            functions.turn_right_on()

        elif "blinker_rechts_off" in form:
            functions.turn_signal_off()

        elif "blaulicht" in form:
            functions.blue_light_on()

        elif "blaulicht_off" in form:
            functions.blue_light_off()

        elif "tagfahrlicht" in form:
            functions.day_light_on()

        elif "tagfahrlicht_off" in form:
            functions.day_light_off()

        elif "scheinwerfer" in form:
            functions.headlights_on()
                
        elif "scheinwerfer_off" in form:
            functions.headlights_off()

        elif "reverse" in form:
            functions.back_driving_lights_on()
            functions.parking_on()
                
        elif "drive" in form:
            functions.back_driving_lights_off()
            functions.parking_off()

        elif "sirene" in request.form:
            functions.siren_on()
        elif "sirene_off" in request.form:
            functions.siren_off()


    return render_template(
        "control.html",
        **functions.get_status()
        )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)
