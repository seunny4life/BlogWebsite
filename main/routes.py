import os
import secrets
from flask import redirect, flash, url_for, render_template, request
from main import app, db
from main.forms import *
from flask_login import current_user, confirm_login, login_user, logout_user, login_required
from main.models import Blog, Post


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    flash("Welcome now")
    return render_template('home.html', title='Home', posts=posts)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return render_template('home.html', isHome=True, title="Home")
    form = LoginForm()
    # Create variable for easy access
    if form.validate_on_submit():
        users = Blog.query.filter_by(username=form.username.data).first()
        if users is None or not users.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for('login'))
        login_user(users, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login In', form=form)


@app.route("/register/", methods=["POST", "GET"])
def register():
    form = RegistationForm()
    if form.validate_on_submit():
        if Blog.query.filter_by(username=form.username.data, email=form.email.data).first():
            flash('You already Registered')
            return redirect(url_for('login'))
        else:
            users = Blog(username=form.username.data,
                        email=form.email.data)
            users.set_password(form.password.data)
            db.session.add(users)
            db.session.commit()
            flash('Welcome, you successful registered')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, isRegister=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title="Profile")


@app.route('/edit_Email', methods=['POST', 'GET'])
@login_required
def edit_Email():
    form = EditEmailForm()
    if form.validate_on_submit():
        if Blog.query.filter_by(email=form.email.data).first():
            flash('Email already taken')
            return redirect(url_for('edit_Email'))
        else:
            current_user.email=form.email.data
            db.session.commit()
            return redirect (url_for('profile'))            
    return render_template('edit_Email.html', title="EditEmail", form=form)



@app.route('/updateprofile', methods=['POST', 'GET'])
@login_required
def updateprofile():
    form = UpdateProfile()
    if form.validate_on_submit():
        current_user.about_me=form.about_me.data
        current_user.location=form.location.data
        current_user.country=form.about_me.data
        db.session.commit()
        return redirect (url_for('profile'))            
    return render_template('updateprofile.html', title="Update Profile", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_bytes(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn= random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route('/pictures', methods=['POST', 'GET'])
@login_required
def pictures():
    form = ChangePicturesForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = image_file
        db.session.commit()
        return redirect (url_for('profile'))            
    return render_template('pictures.html', title="Update Picture", form=form)



@app.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Post created')
        return redirect (url_for('home'))
    return render_template('create_post.html', title="Create Post", form=form)

