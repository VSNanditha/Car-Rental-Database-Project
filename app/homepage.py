import datetime

from flask import (
    Blueprint, render_template, session, request, redirect, url_for, flash
)

from app.db import get_db

homepage = Blueprint('homepage', __name__, url_prefix='/home')
db, conn = get_db()
today = datetime.datetime.now()


@homepage.route('/search', methods=('GET', 'POST'))
def search():
    car_type = session['car_type']
    db.execute('SELECT DISTINCT MAKE FROM CAR WHERE TYPE = (%s) ORDER BY MAKE', (car_type,))
    car_make_list = db.fetchall()
    db.execute('SELECT * FROM CAR INNER JOIN RENTAL_RATES ON CAR.TYPE = RENTAL_RATES.TYPE '
               'WHERE CAR.TYPE = (%s) AND (CAR.CAR_ID) NOT IN (SELECT CAR_ID FROM RENTAL_REQUEST WHERE '
               'RENTAL_REQUEST.CAR_ID = CAR.CAR_ID AND DATE(RENT_END_DATE) <= (%s)) ORDER BY MAKE, MODEL',
               (car_type, session['pickup_date'],))
    car_list = db.fetchall()
    if request.method == 'POST':
        car_make = request.form['car_make']
        if car_make is not None:
            session['car_make'] = car_make
            return redirect(url_for('homepage.brand_search'))
    return render_template('home/search.html', car_list=car_list, car_make_list=car_make_list,
                           template_folder='templates')


@homepage.route('/brand_search')
def brand_search():
    car_type = session['car_type']
    car_make = session['car_make']
    db.execute('SELECT * FROM CAR INNER JOIN RENTAL_RATES ON CAR.TYPE = RENTAL_RATES.TYPE '
               'WHERE CAR.TYPE = (%s) AND MAKE = (%s) AND (CAR_ID) NOT IN (SELECT CAR_ID FROM RENTAL_REQUEST WHERE '
               'RENTAL_REQUEST.CAR_ID = CAR.CAR_ID AND DATE(RENT_END_DATE) <= (%s)) ORDER BY MODEL',
               (car_type, car_make, session['pickup_date'],))
    car_list = db.fetchall()
    return render_template('home/brand_search.html', car_list=car_list, template_folder='templates')


@homepage.route('/book', methods=('GET', 'POST'))
def book():
    session['make'] = request.values['make']
    session['model'] = request.values['model']
    session['price'] = float(request.values['price'])
    if 'user_id' not in session.keys():
        flash('Please login/sign up to continue!!')
        return redirect(url_for('auth.login'))
    else:
        days = (session['drop_date'] - session['pickup_date']).days
        total_price = session['price'] * days
        print('values: ', session, total_price)
        if request.method == 'POST':
            db.execute('SELECT * FROM CAR WHERE MAKE = (%s) AND MODEL = (%s)', (session['make'], session['model'],))
            car = db.fetchone()
            pickup_time = datetime.datetime.strptime(session['pickup_time'], '%H:%M').time()
            db.execute('INSERT INTO RENTAL_REQUEST (CUSTOMER_ID, CAR_ID, APPROVED_BY, RENT_START_DATE, '
                       'RENT_END_DATE, DAYS, RATE_APPLIED, ORDER_TOTAL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                       (session['id'], car['CAR_ID'], '171023',
                        datetime.datetime.combine(session['pickup_date'], pickup_time),
                        datetime.datetime.combine(session['drop_date'], pickup_time), days,
                        session['price'], total_price))
            conn.commit()
            # db.session.commit()
            return redirect(url_for('site.home'))

        return render_template('home/book.html', total_price=total_price, template_folder='templates')
