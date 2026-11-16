from flask import Flask, render_template, redirect, url_for, request
import functions
from jinja2 import Environment

app = Flask(__name__)


@app.post("/brakelight/an")
def brake_light_on():
    functions.break_light_on()
    return "", 204

@app.post("/brakelight/off")
def brake_light_off():
    functions.break_light_off()
    return "", 204

@app.route('/', methods=["GET", "POST"])
def control():

    if request.method == "POST":
        if "warnblink" in request.form:
            if not functions.warn_light_on.is_set():
                functions.warn_light_on()
        elif "warnblink_off" in request.form:
            functions.warn_licht_off()

        elif "blinker_links" in request.form:
            if not functions.is_turn_left_on == True:
                functions.turn_left_on()
        elif "blinker_links_off" in request.form:
            functions.turn_signal_off()

        elif "blinker_rechts" in request.form:
            if not functions.is_turn_right_on == True:
                functions.turn_right_on()
        elif "blinker_rechts_off" in request.form:
            functions.turn_signal_off()
            
        
        #elif "backwards_button" in request.form:
            #if not functions.backwards_on.is_set():
                #functions.backwards_on()
        #elif "backwards_button_off" in request.form:
            #functions.backwards.off()


        elif "blaulicht" in request.form:
            if not functions.blue_light_on.is_set():
                functions.blue_light_on()
        elif "blaulicht_off" in request.form:
            functions.blue_light_off()
        

        #elif "sirene" in request.form:
            #if not functions.sirene_on.is_set():
                #functions.sirene_on()
        #elif "sirene_off" in request.form:
            #functions.sirene_off()
 

        elif "tagfahrlicht" in request.form:
            if not functions.day_light_on.is_set():
                functions.day_light_on()
        elif "tagfahrlicht_off" in request.form:
            functions.day_light_off()

        elif "scheinwerfer" in request.form:
            if not functions.is_headlights_on == True:
                functions.headlights_on()
        elif "scheinwerfer_off" in request.form:
            functions.headlights_off()

        functions.headlights_auto_on()
        functions.headligths_auto_off()

    return render_template(
        "control.html",
        warnblink_activated = functions._warn_light_thread.is_alive(),
        blinker_links_activated = functions.is_turn_left_on == True,
        blinker_rechts_activated = functions.is_turn_right_on == True,
        blaulicht_activated = functions._blue_light_thread.is_alive(),
        #sirene_activated = functions.sirene_deactivated,##### Not done
        tagfahrlicht_activated = functions.day_light_on.is_set(),
        scheinwerfer_activated = functions.is_headlights_on == True,
        #policecar_locked = functions.policecar_locked,
        #reverse = functions.backwards_button.is_set()
        )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

