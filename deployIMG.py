from flask import Flask,render_template,request,jsonify
app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


from mainIMG import generate_responseimg
from main import generate_response
###################################################### START ########################
app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user_system'

mysql = MySQL(app)

##################### CLASS USERS #######################
class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role
##################### END OF CLASS USERS #######################
@app.get('/home')
def index_get():
    user = None
    if 'userid' in session:
        user = User(session['userid'],session['name'])
        if user.role == 'admin':
            return redirect('panel')

    return render_template('imgtest.html')

@app.post('/predictxt')
def get_response():
    text = request.get_json().get("message")
    response = generate_response(text)
    message = {"answer": response}

    return jsonify(message)

@app.post('/predictimg')
def get_responseimg():
    text = request.get_json().get("message")
    response = generate_responseimg(text)
    message = {"answer": response}

    return jsonify(message)





@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']


            mesage = 'Logged in successfully !'
            user = None
            if 'userid' in session:
                user = User(session['userid'], session['name'])
                if user.role == 'admin':
                    return redirect('panel')
                return redirect('home')
        else:
            logedFOR = 0
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return render_template('imgtest.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',(userName, email, password))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage=mesage)
####################### ADMIN PART OF CRUD #####################################################""

@app.route('/panel')
def Index():
    user = None
    if 'userid' in session:
        user = User(session['userid'], session['name'])
        if user.role == 'admin':

            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM users")
            data = cur.fetchall()
            cur.close()
            return render_template('index2.html', students=data )
    return render_template('imgtest.html')


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        password = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE userid=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE users
               SET name=%s, email=%s, password=%s
               WHERE userid=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))




##########################################################################################################################
@app.route('/chat')
def chat():
    user = None
    if 'userid' in session:
        user = User(session['userid'], session['name'])
        return render_template('user.html')
    return render_template('login.html')

@app.route('/store', methods=['GET', 'POST'])
def store():
    return render_template('store.html')

@app.route('/article', methods=['GET', 'POST'])
def article():
    return render_template('blogS.html')
@app.route('/article2', methods=['GET', 'POST'])
def article2():
    return render_template('article2.html')
@app.route('/article3', methods=['GET', 'POST'])
def article3():
    return render_template('article3.html')
@app.route('/article4', methods=['GET', 'POST'])
def article4():
    return render_template('article4.html')

@app.route('/article5', methods=['GET', 'POST'])
def article5():
    return render_template('article5.html')
@app.route('/plans', methods=['GET', 'POST'])
def plans():
    return render_template('plans.html')

if __name__ == "__main__":
    app.run(debug=True)
