from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)


def get_db():
    mysql = MySQL(cursorclass=DictCursor)
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'N@nditha0731'
    app.config['MYSQL_DATABASE_DB'] = 'car_rental'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor, conn
