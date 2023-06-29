from flask import render_template, abort, url_for, redirect, request, session, current_app,flash
from flask_login import current_user, login_required
from . import vlog
from ..decorators import admin_required, blogger_required
from ..models import Picture, Video, Project
from ..forms import PictureForm, VideoForm
from .. import db
import os
import secrets

def save_picture1(thumbnail):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(thumbnail.filename)
    picture_fn = random_hex + f_ext
    basedir = current_app.config['BASEDIR']
    picture_path = os.path.join(basedir, 'app', 'static', 'assets/images/video_thumbnail', picture_fn)
    thumbnail.save(picture_path)

    return picture_fn

@vlog.route("/vlog", methods=['GET', 'POST'])
def vlog_index():
    form = VideoForm()
    if current_user.is_blogger() and form.validate_on_submit():
        thumbnail_file = save_picture1(form.thumbnail.data)
        video = Video(title=form.title.data,
                      thumbnail_file=thumbnail_file,
                      video_link=form.link.data,
                      vlogger=current_user._get_current_object())
        db.session.add(video)
        db.session.commit()
        flash('video created', category='success')
        return redirect(url_for('vlog.vlog_index'))
    page = request.args.get('page', 1, type=int)
    pagination = Video.query.order_by(Video.timestamp.desc()).paginate(
        page=page, per_page=int(current_app.config['VIDEO_PER_PAGE']), error_out=False
    )
    videos = pagination.items
    return render_template('vlog/vlog.html' ,form=form, videos=videos,
                           pagination=pagination)

@vlog.route('/delete_vlog<int:id>')
def delete_vlog(id):
    video = Video.query.get_or_404(id)
    if current_user.is_blogger() or current_user.is_admin():
        db.session.delete(video)
        db.session.commit()
        flash('video deleted', category='info')
        return redirect(url_for('vlog.vlog_index'))
    return redirect(url_for('vlog.vlog_index'))