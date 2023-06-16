from flask import Flask



def create_app():
    app= Flask(__name__)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)

    from .vlog import vlog as vlog_blueprint
    app.register_blueprint(vlog_blueprint)

    from .projects import projects as projects_blueprint
    app.register_blueprint(projects_blueprint)

    return app