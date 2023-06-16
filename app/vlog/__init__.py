from flask import Blueprint

vlog = Blueprint('vlog', __name__)

from . import vlog_views