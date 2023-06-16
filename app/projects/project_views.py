from flask import render_template
from . import projects

@projects.route("/projects")
def projects():
    return render_template('projects.html')