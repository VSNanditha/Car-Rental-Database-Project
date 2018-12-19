from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from app.db import get_db

# from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
db, conn = get_db()


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        license = request.form['license']
        address = request.form['address']
        phone = request.form['phone']
        zip = request.form['zip']

        try:
            db.callproc('signup', (username, license, firstname, lastname, address, zip, phone,
                                   username, password))
            data = db.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect(url_for('auth.login'))
            else:
                print('data: ', data, firstname, lastname, license, address, zip, phone, username, password)
                flash('User Already Exists!!')
        except:
            flash('User Already Exists!!')

    return render_template('auth/signup.html', template_folder='templates')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print(username, password)
        error = None
        db.execute(
            'SELECT * FROM customer WHERE email = (%s)', (username,)
        )
        user = db.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not (user['PASSWORD'] == password):
            error = 'Incorrect password.'

        if error is None:
            session['user_id'] = user['EMAIL']
            session['name'] = user['FIRST_NAME'] + ' ' + user['LAST_NAME']
            session['id'] = user['CUSTOMER_ID']
            session['address'] = user['ADDRESS'] + ', ' + str(user['ZIP_CODE'])
            session['phone'] = user['PHONE_NUMBER']
            # print('session data: ', session, session['user_id'])
            return redirect(url_for('site.home'))

        flash(error)

    return render_template('auth/login.html', active='login', template_folder='templates')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
