from flask import render_template
from . import main

@main.route("/")
def index():
    return render_template("home/home.html")

@main.route("/home")
def home():
    return render_template('home/home.html')

@main.route("/theming")
def theme_stuff():
    return render_template("theming/theming-kit.html")