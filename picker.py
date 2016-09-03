from flask import Flask, render_template, jsonify, request, json, redirect
import random
app = Flask(__name__)

THEMES = "themes.txt"

def rand_line(filename):
    with open(filename) as f:
        lines = f.readlines()
    return random.choice(lines).strip()

@app.route("/")
def cah_filled():
    return render_template("theme.html", theme=rand_line(THEMES))

@app.route("/theme.json")
def cah_json():
    return jsonify({"theme":rand_line(THEMES)})
