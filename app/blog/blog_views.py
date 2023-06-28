from flask import render_template, session, url_for, redirect, flash, request, current_app, abort
from . import blog
from ..forms import NameForm, BlogPostForm
from ..models import User, BlogPost
from .. import db
from ..email import send_email
from flask_login import current_user, login_required
from ..decorators import admin_required, blogger_required



@blog.route("/blog", methods=['GET', 'POST'])
def blog_index():
    form = BlogPostForm()
    if current_user.is_blogger() and form.validate_on_submit():
        post = BlogPost( title=form.title.data, body=form.body.data,
                        author=current_user._get_current_object(),)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.blog_index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = BlogPost.query.order_by(BlogPost.timestamp.desc()).paginate(
        page=page, per_page=int(current_app.config['BLOG_POSTS_PER_PAGE']), error_out=False
    )
    blog_posts = pagination.items
    return render_template('blog/blog.html', form=form, blog_posts=blog_posts,
                           pagination=pagination)


@blog.route("/post<int:id>")
def post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('blog/post.html', blog_posts=[post])

@blog.route("/edit<int:id>", methods=["GET", "POST"])
@login_required
@blogger_required
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if current_user != post.author and not current_user.is_admin():
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash("the post has been updated", category='success')
        return redirect(url_for('blog.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('blog/edit_post.html', form=form)

@blog.route('/delete_blog<int:id>')
@login_required
@blogger_required
def delete(id):
    post = BlogPost.query.get_or_404(id)
    if current_user != post.author and not current_user.is_admin():
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('deleted post' , category='danger')
    return redirect(url_for('blog.blog_index'))

