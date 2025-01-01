from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

# Setup app
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///words.db'
app.config['SECRET_KEY'] = 'secret!'

db = SQLAlchemy(app)

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

# Create a route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Run the web application
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create all columns
    app.run(host='0.0.0.0', port=5555, debug=True)