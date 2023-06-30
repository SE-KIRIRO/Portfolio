from flask import render_template, session, url_for, flash, request, redirect, current_app, abort
from ..forms import ProjectForm, BlogPostForm, EditProjectForm, VideoForm, PictureForm
from ..models import Project, BlogPost, Video, Picture
from .. import db
from . import projects
from flask_login import current_user, login_required
from ..decorators import admin_required, blogger_required
from ..vlog.vlog_views import save_picture1, delete_picture1
import os
import secrets

def save_picture(form_picture):
    randon_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randon_hex + f_ext
    basedir = current_app.config['BASEDIR']
    picture_path = os.path.join(basedir, "app", 'static', 'assets/images/project_background', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

def delete_picture(picture_fn):
    basedir = current_app.config['BASEDIR']
    picture_path = os.path.join(basedir, 'app', 'static/assets/images/project_background', picture_fn)
    os.remove(picture_path)

@projects.route("/pro_image/<image_file>")
def get_image(image_file):
    image = url_for('static', filename='assets/images/project_background/' + image_file, _external=True)
    return image

@projects.route("/projects", methods=['GET', 'POST'])
def projects_index():
    form = ProjectForm()
    if current_user.is_blogger() and form.validate_on_submit():
        picture_file = save_picture(form.framework_pic.data)
        project = Project(title=form.title.data,
                          body=form.body.data,
                          developer=current_user._get_current_object(),
                          image_file=picture_file)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects.projects_index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page=page, per_page=int(current_app.config['PROJECTS_PER_PAGE']), error_out=False
    )
    projects = pagination.items
    return render_template('projects/projects.html', form=form, projects=projects,
                           pagination=pagination)

@projects.route('/project_blog<int:id>', methods=['GET', 'POST'])
@login_required
@blogger_required
def add_project_blog(id):
    project = Project.query.get_or_404(id)
    
    if project:
        form = BlogPostForm()
        if form.validate_on_submit():
            post = BlogPost(title=form.title.data, body=form.body.data,
                            author=current_user._get_current_object(),
                            project_blog=project)
            db.session.add(post)
            db.session.add(project)
            db.session.commit()
            flash('the project blog post has been published', category='success')
            return redirect(url_for('projects.projects_index'))
        return render_template('projects/projects_blog.html', form=form)

@projects.route('/add_project_vlog<int:id>', methods=['GET', 'POST'])
@login_required
@blogger_required
def add_project_vlog(id):
    project = Project.query.get_or_404(id)
    if project:
        form = VideoForm()
        if form.validate_on_submit():
            thumbnail_file = save_picture1(form.thumbnail.data)
            video = Video(title=form.title.data,
                          thumbnail_file=thumbnail_file,
                          video_link=form.link.data,
                          vlogger=current_user._get_current_object(),
                          project_video=project)
            db.session.add(video)
            db.session.add(project)
            db.session.commit()
            flash('the project vlog has been published', category='success')
            return redirect(url_for('projects.projects_index'))
        return render_template('projects/projects_vlog.html', form=form)
    
@projects.route('/add_project_pic<int:id>', methods=['GET', 'POST'])
@login_required
@blogger_required
def add_project_pic(id):
    project = Project.query.get_or_404(id)
    if project:
        form = PictureForm()
        if form.validate_on_submit():
            picture_file = save_picture1(form.picture.data)
            picture = Picture(title=form.title.data,
                              picture_file=picture_file,
                              picman=current_user._get_current_object(),
                              project_pic=project)
            db.session.add(picture)
            db.session.add(project)
            db.session.commit()
            flash('the project pic has been published', category='success')
            return redirect(url_for('projects.projects_index'))
        return render_template('projects/projects_pic.html', form=form)
    
@projects.route('/view_project_pic<int:id>')
def view_project_pic(id):
    project = Project.query.get_or_404(id)
    if project:
        pictures = Picture.query.filter_by(project_pic=project).order_by(Picture.timestamp.desc()).all()
        return render_template('projects/project_pics.html', pictures=pictures)
    
@projects.route('/delete_project_pic<int:id>')
@login_required
@blogger_required
def delete_project_pic(id):
    pic = Picture.query.get_or_404(id)
    if pic:
        delete_picture1(pic.picture_file)
        db.session.delete(pic)
        db.session.commit()
        flash("picture deleted", category='warning')
        return redirect(url_for('projects.projects_index'))



@projects.route('/project_blogs<int:id>')
def view_project_blog(id):
    project = Project.query.get_or_404(id)
    if project:
        blog_posts = BlogPost.query.filter_by(project_blog=project).order_by(BlogPost.timestamp.desc()).all()
        return render_template('projects/project_blogs.html', blog_posts=blog_posts)

@projects.route('/projects_vlogs<int:id>')
def view_project_vlog(id):
    project = Project.query.get_or_404(id)
    if project:
        videos = Video.query.filter_by(project_video=project).order_by(Video.timestamp.desc()).all()
        return render_template('projects/project_vlogs.html', videos=videos)
    
@projects.route('/edit_project<int:id>', methods=['GET','POST'])
@login_required
@blogger_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if current_user.is_blogger():
        form = EditProjectForm()
        if form.validate_on_submit():
            project.title = form.title.data
            project.body = form.body.data
            db.session.add(project)
            db.session.commit()
            flash('the project has been updated', category='success')
            return redirect(url_for('projects.projects_index'))
        form.title.data = project.title
        form.body.data = project.body
        return render_template('projects/edit_project.html', form=form)
    return render_template('home/home.html')


@projects.route('/delete_project<int:id>')
@login_required
@blogger_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if current_user != project.developer and not current_user.is_admin():
        abort(403)
    delete_picture(project.image_file)
    db.session.delete(project)
    db.session.commit()
    flash("project deleted", category='danger')
    return redirect(url_for('projects.projects_index'))