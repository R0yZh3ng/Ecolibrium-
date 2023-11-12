from flask import render_template, redirect, url_for, flash, request, current_app, Response
from flask_login import current_user, login_required

from .forms import CreateForumForm, CreateComments
from .models import Forum, Comment
from app import db

from app.user.models import User

from . import forum_blueprint

import requests

API_URL_LIST = [
    "https://api-inference.huggingface.co/models/Michael-Vptn/ecolibrium", # michael's text sum model
    "https://api-inference.huggingface.co/models/Michael-Vptn/ecolibrium",
    "https://api-inference.huggingface.co/models/Michael-Vptn/ecolibrium",
    "https://api-inference.huggingface.co/models/Michael-Vptn/ecolibrium",
    "https://api-inference.huggingface.co/models/Michael-Vptn/ecolibrium",
    "https://api-inference.huggingface.co/models/Michael-Vptn/ecolibrium",
]

headers = {"Authorization": "Bearer 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"}

global_input_text = ""
global_output_text = "" # api stuff

def divide(input_str, num):
  # Use regular expression to find sentence breaks
  sentence_breaks = [0] + [
    match.end() for match in re.finditer(r'[.!?]\s+', input_str)
  ]
  total_sentences = len(sentence_breaks)

  # Calculate the indices for dividing the sentences
  indices = [
    sentence_breaks[int(total_sentences * i / num)] for i in range(1, num)
  ]

  # Divide the input string into sentences
  strings = []
  start_index = 0
  for index in indices:
    strings.append(input_str[start_index:index])
    start_index = index

  strings.append(input_str[start_index:])  # Add the remaining part
  return strings

def combine(str_list, bullet_type='bullet'):
  if bullet_type == 'bullet':
    bullet = "• \n"
  elif bullet_type == 'number':
    bullet = "1. "
  else:
    bullet = "- "

  combined = "\n".join([f"{bullet}{item}" for item in str_list])
  return combined

def generate(input_text):
  try:
    if len(input_text) > 500:

      input_strings = divide(input_text, len(API_URL_LIST))
      output_segments = [
      ]  # List to store generated text segments from different APIs

      for i in range(len(API_URL_LIST)):
        segment = query({"inputs": input_strings[i]}, API_URL_LIST[i])

        output_segments.append(segment[0]["generated_text"])

        output_text = combine(
          output_segments)  # Combine generated text segments
    else:
      output_text = query(
        {"inputs": input_text},
        API_URL_LIST[0])  # if input is too short, only use one api

      output_text = output_text[0]["generated_text"]

    return output_text
  except Exception as e:
    print(f"generate text error: {e}")
    return "Error: text failed to generate. please try again"


def query(payload, API):  # query payload to APIs
  response = requests.post(API, headers=headers, json=payload)
  return response.json()

@forum_blueprint.route('/delete_comment/<int:forum_id>/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(forum_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if the current user is the creator of the comment
    if current_user.id == comment.creator_id:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully', 'success')
    else:
        flash('You are not authorized to delete this comment', 'danger')

    return redirect(url_for('forum.view_Forum', forum_id=forum_id))

@forum_blueprint.route('/delete_forum/<int:forum_id>', methods=['POST'])
@login_required
def delete_forum(forum_id):
    forum = Forum.query.get_or_404(forum_id)

    # Check if the current user is the creator of the forum post
    if current_user.id == forum.creator_id:
        # Delete the associated comments
        Comment.query.filter_by(forum_id=forum.id).delete()

        # Delete the forum post itself
        db.session.delete(forum)
        db.session.commit()

        flash('Forum post and associated comments deleted successfully', 'success')
    else:
        flash('You are not authorized to delete this forum post', 'danger')

    return redirect(url_for('forum.home'))

@forum_blueprint.route('/home')
@login_required
def home():

    user_id = current_user.id
    user_all_forums = Forum.query.options(db.joinedload(Forum.creator)).filter_by(creator_id=current_user.id).all()
    all_forums = Forum.query.options(db.joinedload(Forum.creator)).all()
    user = User.query.get_or_404(user_id)

    return render_template('forums/home.html', all_forums=all_forums, user = user, user_all_forums=user_all_forums)


@forum_blueprint.route('/view_Forum/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def view_Forum(forum_id):
    forum = Forum.query.get_or_404(forum_id)

    if request.method == 'POST':
        comment_title = request.form.get('comment_title')
        comment_description = request.form.get('comment_description')

        if comment_title and comment_description:
            new_comment = Comment(title=comment_title, description=comment_description, creator_id=current_user.id, forum=forum)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
            return redirect(url_for('forum.view_Forum', forum_id=forum.id))

    all_comments = forum.comments

    return render_template('forums/view_forum.html', forum=forum, all_comments=all_comments)

def calc():
    forum = Forum.query.all()
    totalSaved = Forum.kilo
    
    for kilo in totalSaved:
        kilo+=kilo

    return kilo


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
       errord = True
       desc = ""
       while errord:
          desc = generate(form.content.data)
          if "Error" not in desc:
             errord = False # attempt to generate desc untill no error is throwm
       forum = Forum(
           title=form.title.data,
           description=desc,
           content=form.content.data,
           creator_id=current_user.id,
           kilo = 0.1
       )
       db.session.add(forum)
       db.session.flush()
       db.session.commit()

       return redirect(url_for('forum.home'))
  
   return render_template('forums/create_forum.html', form=form)# creates a new post

def view_forums(): # debug
    comments = Comment.query.all()  # Adjust this query based on your data model
    print(comments)


@forum_blueprint.route('/create_Comment/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def create_Comment(forum_id):
   form = CreateComments()
   user = current_user
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
  
   return render_template('forums/createComment.html', form = form, user = user, forum = forum)# this def creates new flashcards in the set selected
