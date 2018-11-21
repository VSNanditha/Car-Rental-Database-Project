from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM customer WHERE email = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO customer (email, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', template_folder='templates')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        db = get_db()
        error = None
        db.execute(
            'SELECT * FROM customer WHERE email = (%s)', (username,)
        )
        user = db.fetchone()

        print(user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(generate_password_hash(user['PASSWORD']), generate_password_hash(password)):
            print('password: ', user['PASSWORD'], password, check_password_hash(user['PASSWORD'], password), type(user['PASSWORD']), type(password), len(user['PASSWORD']), len(password))
            print(generate_password_hash(user['PASSWORD']), generate_password_hash(password))
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', template_folder='templates')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
