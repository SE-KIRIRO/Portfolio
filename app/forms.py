from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from .models import User
from flask_pagedown.fields import PageDownField
from flask import current_app


class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[DataRequired(), Length(2, 20)])
    email = StringField('enter Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'usernames must have only letters, numbers, dots or underscores')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')
    ])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")
        if (field.data != current_app.config['PORTFOLIO_BLOGGER'] or field.data != current_app.config['PORTFOLIO_ADMIN']):
            raise ValidationError("Invalid Email")
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use') 

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='passwords must match')
    ])
    password2 = PasswordField('confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update password')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='passwords must match')
    ])
    password2 = PasswordField('confirm password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Reset password')

class ChangeEmailForm(FlaskForm):
    email = StringField('New email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('update email address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('email is already registered.')
        

class BlogPostForm(FlaskForm):
    title = StringField("blog title", validators=[DataRequired()])
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField("Share")

class ProjectForm(FlaskForm):
    title = StringField('project title', validators=[DataRequired()])
    body = PageDownField("a short description", validators=[DataRequired()])
    framework_pic = FileField('upload framework logo', validators= [ FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    submit = SubmitField("publish")

class EditProjectForm(FlaskForm):
    title = StringField('project title', validators=[DataRequired()])
    body = PageDownField('a short description ', validators=[DataRequired()])
    submit= SubmitField("submit changes")


class VideoForm(FlaskForm):
    title = StringField("video title", validators=[DataRequired()])
    thumbnail = FileField("upload video thumbnail", validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    link = StringField('video link', validators=[DataRequired()])
    submit = SubmitField("publish video")

class PictureForm(FlaskForm):
    title = StringField("picture title", validators=[DataRequired()])
    picture = FileField("upload a picture", validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    submit = SubmitField("publish picture")