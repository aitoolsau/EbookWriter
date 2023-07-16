from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'zxcveqrgvvZXCvbzxcvb'  # Replace 'your_secret_key' with your actual secret key

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
            session['username'] = username  # Store the username in the session
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

@app.route('/logout')
def logout():
    # Add your logout logic here
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        author_role = request.form.get('author_role')
        author_tone = request.form.get('author_tone')
        username = session['username']
        initial_prompt = request.form.get('initial_prompt')
        task = request.form.get('task')
        topic = request.form.get('topic')
        style = request.form.get('style')
        audience = request.form.get('audience')
        length = request.form.get('length')
        format = request.form.get('format')
        additional_information = request.form.get('additional_information')

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO projects (Title, Description, AuthorRole, AuthorTone, Username, InitialPrompt, Task, Topic, Style, Audience, Length, Format, AdditionalInformation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''', (title, description, author_role, author_tone, username, initial_prompt, task, topic, style, audience, length, format, additional_information))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('projects'))
    else:
        return render_template('add_project.html')

@app.route('/projects')
def projects():
    if 'username' not in session:
        return redirect(url_for('login'))

    from MySQLdb import cursors
    cursor = mysql.connection.cursor(cursors.DictCursor)
    cursor.execute(''' SELECT * FROM projects WHERE Username = %s ''', (session['username'],))
    projects = cursor.fetchall()
    cursor.close()

    print("Projects fetched from database: ", projects)  # Debug print statement

    return render_template('projects.html', projects=projects)

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    from MySQLdb.cursors import DictCursor
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute(''' SELECT * FROM projects WHERE ProjectID = %s ''', (project_id,))
    project = cursor.fetchone()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        author_role = request.form.get('author_role')
        author_tone = request.form.get('author_tone')
        initial_prompt = request.form.get('initial_prompt')

        cursor.execute(''' UPDATE projects SET Title = %s, Description = %s, AuthorRole = %s, AuthorTone = %s, InitialPrompt = %s WHERE ProjectID = %s ''', (title, description, author_role, author_tone, initial_prompt, project_id))
        mysql.connection.commit()

        cursor.close()
        return redirect(url_for('projects'))
    else:
        cursor.close()
        return render_template('edit_project.html', project=project)

@app.route('/generator/<int:project_id>', methods=['GET'])
def generator(project_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    from MySQLdb.cursors import DictCursor
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute(''' SELECT * FROM projects WHERE ProjectID = %s ''', (project_id,))
    project = cursor.fetchone()
    cursor.close()

    return render_template('generator.html', project=project)

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM projects WHERE ProjectID = %s ''', (project_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('projects'))

@app.route('/writers')
def writers():
    if 'username' not in session:
        return redirect(url_for('login'))

    from MySQLdb.cursors import DictCursor
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute(''' SELECT * FROM users WHERE username = %s ''', (session['username'],))
    user = cursor.fetchone()
    cursor.execute(''' SELECT * FROM writers WHERE UserID = %s ''', (user['UserID'],))
    writers = cursor.fetchall()
    cursor.close()

    return render_template('writers.html', writers=writers)

if __name__ == '__main__':
    app.run(debug=True)
