from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#create flask instance
app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "my super secret key"

#connect to mysql db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'admission'
 
mysql = MySQL(app)


#create route decorator
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            user=request.form.get('username')
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and  'first_name' in request.form and 'second_name' in request.form and 'second_name' in request.form and 'password' in request.form and 'email' in request.form and 'contact' in request.form :
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        
        # phone = request.form['phone']
        # age = request.form['age']
        # gender = request.form['gender']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not first_name or not second_name or not username or not password or not email or not contact  :
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO login(username,password,email) VALUES ( % s, % s, % s)', (username, password, email, ))
            cursor.execute('INSERT INTO user(name,email,phone,age,gender) VALUES ( % s, % s, % s, % s, % s)', (username, email, phone, age, gender))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


# @app.route('/dashboard')
# def dashboard():
#     #print('success')
#     cursor=mysql.connection.cursor()
#     user=session['username']
#     #print(user)
#     cursor.execute("select * from user where name=%s",(user, ))
#     data= cursor.fetchone()
#     #print(data)
#     return render_template('dashboard.html',data=data)


# @app.route('/bank', methods =['GET', 'POST'])
# def bank():
#     msg=''
#     if request.method == 'POST' and 'username' in request.form and 'bank' in request.form and 'acc_no' in request.form and 'acc_type' in request.form and 'balance' in request.form :
#         username = request.form['username']
#         bank = request.form['bank']
#         acc_no = request.form['acc_no']
#         acc_type = request.form['acc_type']
#         balance = request.form['balance']
        
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
#         b = cursor.fetchone()
#         if b:
#             msg = 'Account already exists !'
#         elif not username or not bank or not acc_no or not acc_type or not balance :
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO accounts(username,bank,acc_no,acc_type,balance) VALUES ( % s, % s, % s, % s, % s)', (username, bank, acc_no, acc_type, balance))
#             mysql.connection.commit()
#             msg = 'You have successfully added your Bank details !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('bank.html', msg = msg)


# @app.route('/view_bank')
# def view_bank():
#     #print('success')
#     cursor=mysql.connection.cursor()
#     user=session['username']
#     #print(id)
#     cursor.execute("select * from accounts where username=%s",(user, ))
#     bdata= cursor.fetchone()
#     #print(bdata)
#     return render_template('view_bank.html',bdata=bdata)


if __name__ == "__main__":
    app.run(debug=True)