from app import create_app, db
from app.models import Role, User
from flask_migrate import Migrate
import secrets
import os

app = create_app('default')
migrate = Migrate(app, db)




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)