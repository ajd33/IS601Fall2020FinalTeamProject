from flask import Flask, render_template, request, redirect, Response, session
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import secrets
import simplejson as json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'finalApp'
mysql.init_app(app)

app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'
app.config['MAIL_DEFAULT_SENDER'] = 'jj79@njit.edu'
mail = Mail(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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
    cursor = mysql.get_db().cursor()
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
    cursor = mysql.get_db().cursor()
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
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE id=%s', req.get('email').strip())
    result = cursor.fetchall()
    if len(result) != 0:
        return render_template('signup.html', message={'text': 'User already exists'})
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (first_name,last_name,email,password_hash,validation_token) VALUES (%s,%s,%s,%s,%s)"
    val = (
        req.get('first_name'), req.get('last_name'), req.get('email'), password_hash, url_token)
    cursor.execute(sql, val)
    mysql.get_db().commit()
    send_verification(url_token, req.get('email').strip())
    return render_template('verify.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
