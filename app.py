from flask import Flask, render_template, jsonify, send_file, request
import os
import json
from update import update
import threading
import time
import notify

app = Flask(__name__)

with open("course_abbreviations.json", "r") as abbreviations_file:
    course_abbreviations = json.load(abbreviations_file)


def run_update_task(delay_seconds):
    while True:
        time.sleep(delay_seconds)
        update()
        text = "Course data was updated at " + time.strftime("%H:%M:%S %d.%m.%Y") + "."
        subject = "ITU Dersçi Course Data was Updated"
        notify.by_email_update(subject, text)


delay_seconds = 15 * 60

update_thread = threading.Thread(target=run_update_task, args=(delay_seconds,))
update_thread.daemon = True
update_thread.start()


@app.route("/")
def index():
    return render_template("index.html", course_abbreviations=course_abbreviations)


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_file(os.path.join("static", filename))


@app.route("/get_course_data/<course_abbreviation>")
def get_course_data(course_abbreviation):
    json_file_path = os.path.join(
        "course_data", f"course_data_{course_abbreviation}.json"
    )
    try:
        return send_file(json_file_path, mimetype="application/json")
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
