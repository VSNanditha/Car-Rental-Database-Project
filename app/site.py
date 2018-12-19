import datetime

from flask import (
    Blueprint, render_template, session, redirect, url_for, request, flash
)

from app.db import get_db

site = Blueprint('site', __name__, url_prefix='/')
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)
db, conn = get_db()


@site.route('/home', methods=('GET', 'POST'))
def home():
    db.execute('SELECT DISTINCT TYPE FROM RENTAL_RATES;')
    car_types = db.fetchall()
    if request.method == 'POST':
        car_type = request.form['car_type']
        pickup_date = datetime.datetime.strptime(request.form['pickup_date'], '%Y-%m-%d')
        drop_date = datetime.datetime.strptime(request.form['drop_date'], '%Y-%m-%d')
        if drop_date <= pickup_date:
            flash('Check Pick-Up and Drop dates!!')
            return render_template('site/home.html', active='home', today=today.date(), tomorrow=tomorrow.date(),
                                   car_types=car_types, template_folder='templates')
        if car_type is not None:
            session['car_type'] = car_type
            session['pickup_date'] = pickup_date
            session['drop_date'] = drop_date
            session['pickup_time'] = request.form['pickup_time']
            # print('session values: ', session, session['pickup_date'] < session['drop_date'])
            return redirect(url_for('homepage.search'))
    return render_template('site/home.html', active='home', today=today.date(), tomorrow=tomorrow.date(),
                           car_types=car_types, template_folder='templates')


@site.route('/about')
def about():
    return render_template('site/about.html', active='about', template_folder='templates')


@site.route('/booking_history', methods=('GET', 'POST'))
def booking_history():
    db.execute('SELECT * FROM RENTAL_REQUEST INNER JOIN CAR ON CAR.CAR_ID = RENTAL_REQUEST.CAR_ID '
               'WHERE CUSTOMER_ID = (%s) AND RENT_END_DATE >= (%s)', (session['id'], today,))
    current_order_list = db.fetchall()
    db.execute('SELECT * FROM RENTAL_REQUEST INNER JOIN CAR ON CAR.CAR_ID = RENTAL_REQUEST.CAR_ID '
               'WHERE CUSTOMER_ID = (%s) AND RENT_END_DATE < (%s)', (session['id'], today,))
    previous_order_list = db.fetchall()
    print('current_order_list: ', current_order_list, previous_order_list, today)
    return render_template('site/booking_history.html', current_order_list=current_order_list,
                           previous_order_list=previous_order_list)
