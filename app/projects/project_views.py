from flask import render_template, session, url_for, flash, request, redirect, current_app, abort
from ..forms import ProjectForm, BlogPostForm, EditProjectForm
from ..models import Project, BlogPost
from .. import db
from . import projects
from flask_login import current_user, login_required
from ..decorators import admin_required, blogger_required
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

@projects.route("/pro_image/<image_file>")
def get_image(image_file):
    image = url_for('static', filename='assets/images/project_background/' + image_file, _external=True)
    return image

@projects.route("/projects", methods=['GET', 'POST'])
def projects_index():
    form = ProjectForm()
    if current_user.is_blogger and form.validate_on_submit():
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
        

@projects.route('/project_blogs<int:id>', methods=['GET', 'POST'])
def view_project_blog(id):
    project = Project.query.get_or_404(id)
    if project:
        page = request.args.get('page', 1, type=int)
        pagination = BlogPost.query.order_by(BlogPost.timestamp.desc()).paginate(
            page=page, per_page=int(current_app.config['BLOG_POSTS_PER_PAGE']), error_out=False
        )
        blog_posts = pagination.items
        return render_template('projects/project_blogs.html', blog_posts=blog_posts,
                               pagination=pagination)
    
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
    db.session.delete(project)
    db.session.commit()
    flash("project deleted", category='danger')
    return redirect(url_for('projects.projects_index'))