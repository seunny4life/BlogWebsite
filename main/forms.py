from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, SubmitField, StringField, RadioField, IntegerField
from wtforms.validators import DataRequired, ValidationError,  EqualTo, Email, Length
from wtforms import FormField, DateField,  PasswordField, TextAreaField
from main.models import Blog


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login In')


class RegistationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(),
                EqualTo('password', message='Password must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        users = Blog.query.filter_by(username=username.data).first()
        if users is not None:
            raise ValidationError('Please a different username.')

    def validate_email(self, email):
        users = Blog.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('Please a different email.')


class EditEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        users = Blog.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('Please a different email.')

class UpdateProfile(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    location = StringField('Location', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Update')

class ChangePassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired(),
                                                   EqualTo('password', message='Password must match')])
    submit = SubmitField('Submit')

    def __init__(self, original_password, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.original_password = original_password

    def validate_password(self, password):
        if password.data != self.original_password:
            user = Blog.query.filter_by(
                password=self.password.data).first()
            if user is not None:
                raise ValidationError('Choose another Password')

class ChangePicturesForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')