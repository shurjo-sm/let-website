from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class NewsPostForm(FlaskForm):
	title = StringField('Post Title', validators=[DataRequired(), Length(min=1, max=200)])
	body = TextAreaField('Post Body', validators=[DataRequired(), Length(min=1, max=4000)])
	submit = SubmitField('Submit Post')

class SecurePostForm(FlaskForm):
	title = StringField('Post Title', validators=[DataRequired(), Length(min=1, max=200)])
	body = TextAreaField('Post Body', validators=[DataRequired(), Length(min=1, max=4000)])
	submit = SubmitField('Submit Post')