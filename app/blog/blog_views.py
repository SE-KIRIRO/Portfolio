from flask import render_template
from . import blog

@blog.route("/blog")
def blog():
    return render_template('blog.html')