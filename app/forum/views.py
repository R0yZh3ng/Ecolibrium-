from flask import render_template, redirect, url_for, flash, request, current_app, Response
from flask_login import current_user, login_required

from .forms import CreateForumForm, CreateComments
from .models import Forum, Comment
from app import db

from app.user.models import User

from . import forum_blueprint

@forum_blueprint.route('/home')
@login_required
def home():
    print_forums()
    user_all_forums = Forum.query.options(db.joinedload(Forum.creator)).filter_by(creator_id=current_user.id).all()
    all_forums = Forum.query.options(db.joinedload(Forum.creator)).all()

    return render_template('forums/home.html', all_forums=all_forums, user_all_forums=user_all_forums)


@forum_blueprint.route('/view_Forum/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def view_Forum(forum_id):
   forum = Forum.query.get_or_404(forum_id)
   comment = forum.comments

   return render_template('forums/view_forum.html', forum=forum, comment=comment)# use this to diplay the correct forum

@forum_blueprint.route('/pub_view_forum/<int:forum_id>')
def pub_view_Forum(forum_id):
   forum = Forum.query.get_or_404(forum_id)
   comment = Forum.comment
   return render_template('forums/pub_view_forum.html', forum = forum, comment = comment)

@forum_blueprint.route('/create_forum', methods=['GET', 'POST'])
@login_required
def create_forum():
   form = CreateForumForm()
   if form.validate_on_submit():
       forum = Forum(
           name=form.name.data,
           private=form.private.data,
           creator_id=current_user.id
       )
       db.session.add(forum)
       db.session.flush()
       db.session.commit()

       return redirect(url_for('forum.home'))
  
   return render_template('forums/create_forum.html', form=form)# creates a new deck


@forum_blueprint.route('/create_Comment/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def create_Flash_Cards(forum_id):

   form = CreateComments()
   if form.validate_on_submit():
       comment = Comment(
           title = form.title.data,
           description = form.description.data,
           forum_id= forum_id,
           creator_id=current_user.id
   )
       db.session.add(comment)
       db.session.commit()
       flash('Comment successfully added to the forum')

       return redirect(url_for('forum.view_forum', forum_id = forum_id))
  
   return render_template('forums/createComment.html', form = form)# this def creates new flashcards in the set selected

def print_forums():
     all_forums = Forum.query.all()
     for forum in all_forums:
       print(f"Forum ID: {forum.id}, Forum title: {forum.title}, Creator ID: {forum.creator_id}")# debug