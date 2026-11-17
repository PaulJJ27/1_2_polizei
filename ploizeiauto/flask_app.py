from flask import Flask, render_template, redirect, url_for, request
import functions
from jinja2 import Environment
import RFID_Sensor
import temp_functions

app = Flask(__name__)

@app.post("/brakelight/an")
def brake_light_on():
    functions.brakes_light_on()
    return "", 204

@app.post("/brakelight/off")
def brake_light_off():
    functions.brakes_light_off()
    return "", 204


@app.route('/', methods=["GET", "POST"])
def control():

    if request.method == "POST":
        form = request.form

        if "warnblink" in form:
            functions.warn_light_on()

        elif "warnblink_off" in form:
            functions.warn_light_off()

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

        elif "backwards_button" in form:
            functions.back_driving_lights_on()
            functions.parking_on()
                
        elif "backwards_button_off" in form:
            functions.back_driving_lights_off()
            functions.parking_off()

       # elif "sirene" in request.form:
            #temp_functions.sirene_on()
        #elif "sirene_off" in request.form:
            #temp_functions.sirene_off()

        elif "rfid_button" in form:
            RFID_Sensor.key_check()
            if RFID_Sensor.is_unlocked == True:
                functions.day_light_on()
                functions.rear_light_on()
                functions.headlights_auto_on()

        elif RFID_Sensor.is_unlocked == False:
            functions.turn_off()

        


    return render_template(
        "control.html",
        **functions.get_status()
        )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)


