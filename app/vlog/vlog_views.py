from flask import render_template
from . import vlog

@vlog.route("/vlog")
def vlog():
    return render_template('vlog.html')