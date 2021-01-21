from main import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(blog_id):
      return Blog.query.get(int(blog_id))


class Blog(UserMixin, db.Model):
      __tablename__ = 'blog'

      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(100), nullable=False, unique=True, index=True)
      password_hash = db.Column(db.String(300), nullable=False)
      email = db.Column(db.String(300), nullable=False, index=True, unique=True)
      location = db.Column(db.Text)
      country = db.Column(db.Text)
      gender = db.Column(db.String(20))
      date_of_birth = db.Column(db.DateTime)
      about_me = db.Column(db.String(300))
      last_seen = db.Column(db.DateTime, default=datetime.utcnow)
      posts = db.relationship('Post', backref='author', lazy='dynamic')
      image_file = db.Column(db.String(50), nullable=False, default="default.jpg")

      def save_to_db(self):
        db.session.add(self)
        db.session.commit()

      def set_password(self, password):
            self.password_hash = generate_password_hash(password)

      def check_password(self, password):
            return check_password_hash(self.password_hash, password)

      def __repr__(self):
            return '<Blog {}>'.format(self.username)
      

class Post(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100), nullable=False)
      content = db.Column(db.Text, nullable=False)
      date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
      blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

      def __repr__(self):
            return '<Post {}>'.format(self.body)
