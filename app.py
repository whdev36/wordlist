from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Setup app
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///words.db'
app.config['SECRET_KEY'] = 'secret!'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create a model for user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Create a model for words
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable=False)
    pronunciation = db.Column(db.String(255))
    meaning = db.Column(db.String(255))

# Create form
class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired(), Length(min=1, max=255)])
    pronunciation = StringField('Pronunciation', validators=[Length(min=1, max=255)])
    meaning = StringField('Meaning', validators=[Length(min=1, max=255)])
    submit = SubmitField('Submit')

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create a route for admin
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    form = WordForm()
    if form.validate_on_submit():
        word = form.word.data
        pronunciation = form.pronunciation.data
        meaning = form.meaning.data
        return redirect(url_for('admin'))

    return render_template('admin.html', form=form)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('admin'))
    return render_template('login.html', form=form)

# Logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create a route for homepage
@app.route('/')
def index():
    # form = 
    return render_template('index.html')

# Run the web application
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create all columns
    app.run(host='0.0.0.0', port=5555, debug=True)