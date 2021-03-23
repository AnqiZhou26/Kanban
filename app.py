import os
import sqlite3
from flask import Flask, g, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'anqizhou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    removed = db.Column(db.Boolean)

db.create_all()
db.session.commit()


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password_entered = request.form['password']

        if not all([user_name, password_entered]):
            # if username/password is null, or are both null
            return redirect(url_for('login'))

        user = User.query.filter_by(username=user_name).first()
        # the username does not exist
        if not user:
            return redirect(url_for('signup'))
        # successful sign in
        if user and user.password == password_entered:
            next_page = request.args.get('next')
            login_user(user)
            return redirect(next_page) if next_page else redirect('/')
        # if the username exists but the password is incorrect
        if user and user.password != password_entered:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/')
@login_required
def index():
    incomplete = Todo.query.filter_by(removed=False).filter_by(status='incomplete').all()
    ongoing = Todo.query.filter_by(removed=False).filter_by(status='ongoing').all()
    complete = Todo.query.filter_by(removed=False).filter_by(status='complete').all()
    removed = Todo.query.filter_by(removed=True).all()

    return render_template('index.html', incomplete=incomplete, ongoing=ongoing, complete=complete, removed=removed)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], status='incomplete', removed=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/ongoing/<id>')
def ongoing(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.status = 'ongoing'
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.status = 'complete'
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/removed/<id>')
def removed(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.removed = True
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
