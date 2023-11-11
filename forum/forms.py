from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CreateForumForm(FlaskForm):
    title = StringField('Forum name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField('Create Deck')


class CreateComments(FlaskForm):
   question = StringField('question', validators = [DataRequired()])
   answer = StringField('answer', validators = [DataRequired()])
   submit = SubmitField('Create flashCard')
