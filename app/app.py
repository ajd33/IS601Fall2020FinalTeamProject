from typing import List, Dict
import simplejson as json
import mysql.connector
from flask import Flask, request, Response, redirect,session
from flask import render_template

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import secrets

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
flask_mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'gasMileage'
flask_mysql.init_app(app)

app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''
mail = Mail(app)

user = {'username': 'IS601 Team'}

class MyDb:
    def __init__(self):
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'gasMileage'
        }
        self.connection = mysql.connector.connect(**config)

    def closeDb(self):
        self.connection.close()

    def get_alldata(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM gasTable')
        return cursor.fetchall()

    def get_mileage(self, mileage_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM gasTable WHERE id=%s', (mileage_id,))
        result = cursor.fetchall()
        return result[0]

    def update_mileage(self, inputData):
        cursor = self.connection.cursor(dictionary=True)
        sql_update_query = """UPDATE gasTable t SET t.Gallons = %s, t.Mileage = %s, t.Price = %s WHERE t.id = %s """
        cursor.execute(sql_update_query, inputData)
        self.connection.commit()

    def insert_mileage(self, inputData):
        cursor = self.connection.cursor(dictionary=True)
        sql_insert_query = """INSERT INTO gasTable (`Gallons`,Mileage,Price) VALUES (%s, %s, %s) """
        cursor.execute(sql_insert_query, inputData)
        self.connection.commit()

    def delete_mileage(self, mileage_id):
        cursor = self.connection.cursor(dictionary=True)
        sql_delete_query = """DELETE FROM gasTable WHERE id = %s """
        cursor.execute(sql_delete_query, (mileage_id,))
        self.connection.commit()


db = MyDb()


@app.route('/')
def index():
    gasTable = db.get_alldata()
    return render_template('index.html', Price='Home', user=user, gasTable=gasTable)

@app.route('/view/<int:mileage_id>', methods=['GET'])
def record_view(mileage_id):
    mileage = db.get_mileage(mileage_id)
    return render_template('view.html', Price='View Form', user=user, mileage=mileage)


@app.route('/edit/<int:mileage_id>', methods=['GET'])
def form_edit_get(mileage_id):
    mileage = db.get_mileage(mileage_id)
    return render_template('edit.html', Price='Edit Form', user=user, mileage=mileage)


@app.route('/edit/<int:mileage_id>', methods=['POST'])
def form_update_post(mileage_id):
    inputData = (request.form.get('Gallons'), request.form.get('Mileage'), request.form.get('Price'), mileage_id)
    db.update_mileage(inputData)
    return redirect("/", code=302)

@app.route('/mileage/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', Price='New Mileage Form', user=user)


@app.route('/mileage/new', methods=['POST'])
def form_insert_post():
    inputData = (request.form.get('Gallons'), request.form.get('Mileage'), request.form.get('Price'))
    db.insert_mileage(inputData)
    return redirect("/", code=302)

@app.route('/delete/<int:mileage_id>', methods=['POST'])
def form_delete_post(mileage_id):
    db.delete_mileage(mileage_id)
    return redirect("/", code=302)

@app.route('/api/v1/mileage')
def api_mileage() -> str:
    js = json.dumps(db.get_alldata())
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/mileages/<int:mileage_id>', methods=['GET'])
def api_retrieve(mileage_id) -> str:
    result = db.get_mileage(mileage_id)
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/mileages/', methods=['POST'])
def api_add() -> str:
    inputData = (request.form.get('Gallons'), request.form.get('Mileage'), request.form.get('Price'))
    db.insert_mileage(inputData)
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/mileages/<int:mileage_id>', methods=['PUT'])
def api_edit(mileage_id) -> str:
    inputData = (request.form.get('Gallons'), request.form.get('Mileage'), request.form.get('Price'), mileage_id)
    db.update_mileage(inputData)
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/mileages/<int:mileage_id>', methods=['DELETE'])
def api_delete(mileage_id) -> str:
    db.delete_mileage(mileage_id)
    resp = Response(status=210, mimetype='application/json')
    return resp


@app.route('/home', methods=['GET'])
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    req = request.form
    password = req.get('password').strip()
    cursor = flask_mysql.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', req.get('email').strip())
    result = cursor.fetchall()
    if len(result) != 0:
        result_pass = result[0]['password_hash']
        if check_password_hash(result_pass, password):
            session['username'] = req.get('email')
            return redirect("/home")
        else:
            return render_template("/login.html", message={'text': 'Authentication Failed'})
    else:
        return render_template("/login.html", message={'text': 'Authentication Failed'})


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


def send_verification(url_token, email):
    msg = Message('IS601 Final Web Application: Verify Email', recipients=[email])
    msg.body = 'Thank you for creating an account with IS601 Final Web Application'
    msg.html = ('<h1>Please validate your email by click on the link given below</h1>'
                'http://127.0.0.1:5000/verify/' + url_token)
    mail.send(msg)


@app.route('/verify/<url_token>', methods=['GET'])
def verify(url_token):
    cursor = flask_mysql.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE validation_token=%s', url_token.strip())
    result = cursor.fetchall()
    if len(result) != 0:
        session['username'] = result[0]['email']
        return redirect('/home')
    else:
        return render_template('index.html')


@app.route('/signup', methods=['POST'])
def create_user():
    req = request.form
    password = req.get('password').strip()
    re_enter_password = req.get('re_enter_password').strip()
    if password != re_enter_password:
        return render_template('signup.html', message={'text': 'Passwords does not match'})
    url_token = secrets.token_urlsafe(16)
    cursor = flask_mysql.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE id=%s', req.get('email').strip())
    result = cursor.fetchall()
    if len(result) != 0:
        return render_template('signup.html', message={'text': 'User already exists'})
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (first_name,last_name,email,password_hash,validation_token) VALUES (%s,%s,%s,%s,%s)"
    val = (
        req.get('first_name'), req.get('last_name'), req.get('email'), password_hash, url_token)
    cursor.execute(sql, val)
    flask_mysql.get_db().commit()
    send_verification(url_token, req.get('email').strip())
    return render_template('verify.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
