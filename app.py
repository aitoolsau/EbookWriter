from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bdm#110044#'
app.config['MYSQL_DB'] = 'aitools_ebookwriter'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM users WHERE username = %s AND password = %s ''', (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        role = request.form.get('role')
        status = request.form.get('status')

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO users (username, password, first_name, second_name, role, status) VALUES (%s, %s, %s, %s, %s, %s) ''', (username, password, first_name, second_name, role, status))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
