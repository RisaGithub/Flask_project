from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):
    name = StringField('Name of course', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TopicForm(FlaskForm):
    name = StringField('Name of topic', validators=[DataRequired()])
    content = TextAreaField('Content of topic', validators=[DataRequired()])
    submit = SubmitField('Submit')