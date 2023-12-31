from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb
from api import openai

app = Flask(__name__)
app.secret_key = 'zxcveqrgvvZXCvbzxcvb'  # Replace 'your_secret_key' with your actual secret key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bdm#110044#'
app.config['MYSQL_DB'] = 'aitools_ebookwriter'

mysql = MySQL(app)

# Define a function to generate text using the OpenAI API
def generate_text(prompt, model='text-davinci-002'):
    # If the prompt is empty, use a default test prompt
    if not prompt:
        prompt = "Translate the following English text to French: '{}'"
    
    # Use the OpenAI API to generate text
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100
    )

    # Return the generated text
    return response.choices[0].text.strip()


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
            session['userID'] = user[0]  # Store the userID in the session
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
        username = session['username']
        initial_prompt = request.form.get('initial_prompt')
        task = request.form.get('task')
        topic = request.form.get('topic')
        style = request.form.get('style')
        tone = request.form.get('tone')
        audience = request.form.get('audience')
        length = request.form.get('length')
        format = request.form.get('format')
        additional_information = request.form.get('additional_information')

        cursor.execute(''' INSERT INTO projects (Title, Description, Username, InitialPrompt, Task, Topic, Style, Audience, Length, Format, AdditionalInformation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''', (title, description, username, initial_prompt, task, topic, style, audience, length, format, additional_information))
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
    print(f"Project: {project}")  # Debug print statement

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        initial_prompt = request.form.get('initial_prompt')

        cursor.execute(''' UPDATE projects SET Title = %s, Description = %s, InitialPrompt = %s WHERE ProjectID = %s ''', (title, description, initial_prompt, project_id))
        mysql.connection.commit()

        cursor.close()
        return redirect(url_for('projects'))
    else:
        cursor.close()
        return render_template('edit_project.html', project=project)

@app.route('/generator/<int:project_id>', methods=['GET', 'POST'])
def generator(project_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    from MySQLdb.cursors import DictCursor
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute(''' SELECT * FROM projects WHERE ProjectID = %s ''', (project_id,))
    project = cursor.fetchone()

    cursor.execute(''' SELECT * FROM writers WHERE UserID = %s ''', (session['userID'],))
    writers = cursor.fetchall()

    cursor.close()

    if request.method == 'POST':
        writer_id = request.form.get('writer')
        for writer in writers:
            if writer['WriterID'] == int(writer_id):
                selected_writer = writer
                break

        print(f"Project: {project}")
        print(f"Selected Writer: {selected_writer}")

        if all(key in project for key in ['Task', 'Topic']) and all(key in selected_writer for key in ['Style', 'Tone', 'Audience', 'Length', 'Format', 'AdditionalInformation']):
            prompt = f"Task: {project['Task']}\nTopic: {project['Topic']}\nStyle: {selected_writer['Style']}\nTone: {selected_writer['Tone']}\nAudience: {selected_writer['Audience']}\nLength: {selected_writer['Length']}\nFormat: {selected_writer['Format']}\nAdditional Information: {selected_writer['AdditionalInformation']}"
        else:
            prompt = "Incomplete data. Please ensure all fields are filled."
        return render_template('generator.html', project=project, writers=writers, prompt=prompt)

    return render_template('generator.html', project=project, writers=writers)

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
    if 'userID' not in session:
        return redirect(url_for('login'))

    from MySQLdb.cursors import DictCursor
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute(''' SELECT * FROM writers WHERE UserID = %s ''', (session['userID'],))
    writers = cursor.fetchall()
    cursor.close()

    return render_template('writers.html', writers=writers)

@app.route('/add_writer', methods=['GET', 'POST'])
def add_writer():
    if 'userID' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        userID = session['userID']
        task = request.form.get('task')
        topic = request.form.get('topic')
        style = request.form.get('style')
        tone = request.form.get('tone')
        audience = request.form.get('audience')
        length = request.form.get('length')
        format = request.form.get('format')
        additional_information = request.form.get('additional_information')

        cursor = mysql.connection.cursor()
        writerName = request.form.get('writerName')
        cursor.execute(''' INSERT INTO writers (UserID, Task, Topic, Style, Tone, Audience, Length, Format, AdditionalInformation, writerName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''', (userID, task, topic, style, tone, audience, length, format, additional_information, writerName))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('writers'))
    else:
        return render_template('add_writer.html')
        return render_template('add_writer.html')

@app.route('/delete_writer/<int:WriterID>', methods=['POST'])
def delete_writer(WriterID):
    if 'userID' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM writers WHERE WriterID = %s ''', (WriterID,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('writers'))

@app.route('/edit_writer/<int:WriterID>', methods=['GET', 'POST'])
def edit_writer(WriterID):
    if 'userID' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(''' SELECT * FROM writers WHERE WriterID = %s ''', [WriterID])
    writer = cursor.fetchone()

    if request.method == 'POST':
        task = request.form.get('task')
        topic = request.form.get('topic')
        style = request.form.get('style')
        tone = request.form.get('tone')
        audience = request.form.get('audience')
        length = request.form.get('length')
        format = request.form.get('format')
        additional_information = request.form.get('additional_information')
        writerName = request.form.get('writerName')

        cursor.execute(''' UPDATE writers SET Task = %s, Topic = %s, Style = %s, Tone = %s, Audience = %s, Length = %s, Format = %s, AdditionalInformation = %s, writerName = %s WHERE WriterID = %s ''', (task, topic, style, tone, audience, length, format, additional_information, writerName, WriterID))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('writers'))
    else:
        return render_template('edit_writer.html', writer=writer)
    


@app.route('/api/sendToOpenAI', methods=['POST'])
def send_to_openai():
    # Get the prompt from the request body
    data = request.get_json()
    prompt = data.get('prompt')

    # Generate text using the OpenAI API
    response = generate_text(prompt)

    # Return the generated text in the response
    return jsonify({'response': response})


@app.route('/test_ai')
def test_ai():
    return render_template('test_ai.html')

if __name__ == '__main__':
    app.run(debug=True)
