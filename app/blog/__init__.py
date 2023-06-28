from flask import Blueprint
from ..models import Permission

blog = Blueprint('blog', __name__)

@blog.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

from . import blog_views