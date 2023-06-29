from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from jose import jwt, JWTError
from flask import current_app, flash, render_template, url_for
import time
from datetime import datetime
from markdown import markdown
import bleach

class Permission:
    BLOGGER = 1
    ADMIN = 2

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def remove_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions -= perm
    
    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    @staticmethod
    def insert_roles():
        roles = {
            "blogger": [Permission.BLOGGER],
            "admin": [Permission.ADMIN, Permission.BLOGGER]
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return f"<Role {self.name}>"
    
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    posts = db.relationship('BlogPost', backref='author', lazy='dynamic')
    projects = db.relationship('Project', backref='developer', lazy='dynamic')
    video = db.relationship("Video", backref='vlogger', lazy='dynamic')
    picture = db.relationship('Picture', backref='picman', lazy='dynamic')
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['PORTFOLIO_ADMIN']:
                self.role = Role.query.filter_by(name='admin').first()
            if self.role is None:
                if self.email == current_app.config['PORTFOLIO_BLOGGER']:
                    self.role = Role.query.filter_by(name='blogger').first()

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self, expiration=3600):
        payload = {
            'confirm': self.id,
            'expires': time.time() + expiration
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        return token
    
    def confirm_tkn(self, token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            expire = data.get('expires')
            if datetime.utcnow() > datetime.utcfromtimestamp(expire):
                return False
            if data.get('confirm') != self.id:
                return False
            self.confirmed = True
            db.session.add(self)
            return True
        except:
            return False
        
    def generate_reset_token(self, expiration=3600):
        payload = {
            'reset': self.id,
            'expires': time.time() + expiration
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        return token
    
    @staticmethod
    def reset_password(token, new_password):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            expire = data.get('expires')
            if datetime.utcnow() > datetime.utcfromtimestamp(expire):
                return False
            user = User.query.get(data.get('reset'))
            if user is None:
                return False
            user.password =  new_password
            db.session.add(user)
            return True
        except:
            return False
        

    def generate_email_change_token(self,new_email, expiration=3600):
        payload = {
            'change_email': self.id,
            'new_email': new_email,
            'expires': time.time() + expiration
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        return token
    
    def change_email(self, token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            expire = data.get('expires')
            if datetime.utcnow() > datetime.utcfromtimestamp(expire):
                return False
            if data.get('change_email') != self.id:
                return False
            new_email = data.get('new_email')
            if new_email is None:
                return False
            if self.query.filter_by(email=new_email).first() is not None:
                return False
            self.email = new_email
            db.session.add(self)
            return True
        except:
            return False
        
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    def is_admin(self):
        return self.can(Permission.ADMIN)
    def is_blogger(self):
        return self.can(Permission.BLOGGER)

    def __repr__(self):
        return f"<User {self.username}>"

    
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_admin(self):
        return False
    def is_blogger(self):
        return False
    
login_manager.anonymous_user = AnonymousUser
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
            'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p'
        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))
db.event.listen(BlogPost.body, 'set', BlogPost.on_changed_body)

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    developer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_file = db.Column(db.String(64), nullable=False)
    blog = db.relationship('BlogPost', backref='project_blog', lazy='dynamic')
    video = db.relationship('Video', backref='project_video', lazy='dynamic')
    picture = db.relationship('Picture', backref='project_pic', lazy='dynamic')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
            'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p'
        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))


db.event.listen(Project.body, 'set', Project.on_changed_body)


class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    thumbnail_file = db.Column(db.String(64), nullable=False)
    video_link = db.Column(db.String(128), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    developer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    picture_file = db.Column(db.String(128), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    developer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
