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
    user_all_forums = Forum.query.options(db.joinedload(Forum.creator)).filter_by(creator_id=current_user.id).all()
    all_forums = Forum.query.options(db.joinedload(Forum.creator)).all()
    username = current_user.username

    return render_template('forums/home.html', all_forums=all_forums, user_all_forums=user_all_forums, username = username)


@forum_blueprint.route('/view_Forum/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def view_Forum(forum_id):
   forum = Forum.query.get_or_404(forum_id)
   all_comments = forum.comments

   #total = calc()
   #don't forget to pass the value into the render_template

   return render_template('forums/view_forum.html', forum=forum, all_comments=all_comments)# use this to diplay the correct forum

# def calc():
#     forum = Forum.query.all()
#     totalSaved = forum.kilo
    
#     for kilo in totalSaved:
#         kilo+=kilo

#     return kilo
    
# This would be the function used to calculate the total kg of emission reduced


@forum_blueprint.route('/pub_view_forum/<int:forum_id>')
def pub_view_Forum(forum_id):
   forum = Forum.query.get_or_404(forum_id)
   comment = Forum.comment
   return render_template('forums/pub_view_forum.html', forum = forum, comment = comment)

@forum_blueprint.route('/create_forum', methods=['GET', 'POST'])
@login_required
def create_forum():
   view_forums()
   form = CreateForumForm()
   if form.validate_on_submit():
       forum = Forum(
           title=form.title.data,
           description=form.description.data,
           creator_id=current_user.id
       )
       db.session.add(forum)
       db.session.flush()
       db.session.commit()

       return redirect(url_for('forum.home'))
  
   return render_template('forums/create_forum.html', form=form)# creates a new deck

def view_forums(): # debug
    comments = Comment.query.all()  # Adjust this query based on your data model
    print(comments)


@forum_blueprint.route('/create_Comment/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def create_Comment(forum_id):
   form = CreateComments()
   forum = Forum.query.get_or_404(forum_id)
   if form.validate_on_submit():
       comment = Comment(
           title = form.title.data,
           description = form.description.data,
           forum_id= forum_id,
           creator_id=current_user.id
   )
       
       db.session.add(comment)
       db.session.flush()
       db.session.commit()
       flash('Comment successfully added to the forum')

       return redirect(url_for('forum.view_Forum', forum = forum, forum_id = forum_id))
  
   return render_template('forums/createComment.html', form = form, forum = forum)# this def creates new flashcards in the set selected
