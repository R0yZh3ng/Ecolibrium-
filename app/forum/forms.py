from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CreateForumForm(FlaskForm):
    title = StringField('Forum name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Deck')


class CreateComments(FlaskForm):
   title = StringField('title', validators = [DataRequired()])
   description = StringField('description', validators = [DataRequired()])
   submit = SubmitField('Create flashCard')
