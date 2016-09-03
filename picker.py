from flask import Flask, render_template, jsonify, request, json, redirect
import random
import os

app = Flask(__name__)

THEMES = os.path.join(os.path.dirname(__file__), "themes.txt")

def rand_line(filename):
    with open(filename) as f:
        lines = f.readlines()
    return unicode(random.choice(lines).strip(), "utf-8")

@app.route("/")
def cah_filled():
    return render_template("theme.html", theme=rand_line(THEMES))

@app.route("/theme.json")
def cah_json():
    return jsonify({"theme":rand_line(THEMES)})
