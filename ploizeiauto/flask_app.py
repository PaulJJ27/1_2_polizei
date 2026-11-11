from flask import Flask, render_template, redirect, url_for, request
import funcs

app = Flask(__name__)


@app.post("/brakelight/an")
def brake_light_on():
    funcs.bremsen_on()
    return "", 204

@app.post("/brakelight/off")
def brake_light_off():
    funcs.bremsen_off()
    return "", 204

@app.route('/', methods=["GET", "POST"])
def control():

    if request.method == "POST":
        if "warnblink" in request.form:
            if not funcs.tag_fahr_licht_on.is_set():
                funcs.tag_fahr_licht_on()
        elif "warnblink_off" in request.form:
            funcs.tag_fahr_licht_off()

        elif "blinker_links" in request.form:
            if not funcs.blinker_links_on.is_set():
                funcs.blinker_links_on()
        elif "blinker_links_off" in request.form:
            funcs.blinker_links_off()

        elif "blinker_rechts" in request.form:
            if not funcs.blinker_rechts_on.is_set():
                funcs.blinker_rechts_on()
        elif "blinker_rechts_off" in request.form:
            funcs.blinker_rechts_off()

        elif "blaulicht" in request.form:
            if not funcs.blau_licht_on.is_set():
                funcs.blau_licht_on()
        elif "blaulicht_off" in request.form:
            funcs.blau_licht_off()

        elif "sirene" in request.form:
            if not funcs.sirene_on.is_set():
                funcs.sirene_on()
        elif "sirene_off" in request.form:
            funcs.sirene_off()

        elif "tagfahrlicht" in request.form:
            if not funcs.tag_fahr_licht_on.is_set():
                funcs.tag_fahr_licht_on()
        elif "tagfahrlicht_off" in request.form:
            funcs.tag_fahr_licht_off()

        elif "scheinwerfer" in request.form:
            if not funcs.scheinwerfer_on.is_set():
                funcs.scheinwerfer_on()
        elif "scheinwerfer_off" in request.form:
            funcs.scheinwerfer_off()

        

    return render_template(
        "control.html",
        warnblink_activated = funcs.tag_fahr_licht_on.is_set(),
        blinker_links_activated = funcs.blinker_links_deactivated,
        blinker_rechts_activated = funcs.blinker_rechts_deactivated,
        blaulicht_activated = funcs.blau_licht_on.is_set(),
        sirene_activated = funcs.sirene_deactivated,
        tagfahrlicht_activated = funcs.tagfahrlicht_deactivated,
        scheinwerfer_activated = funcs.scheinwerfer_deactivated,
        policecar_locked = funcs.policecar_locked
        )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

