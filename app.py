from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Define the connect_to_database function to establish a connection
def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Password is null
        database="student_database"
    )
    return connection

connection = connect_to_database()

def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def validate_password(password):
    return len(password) >= 8

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        f_name = request.form['fname']
        l_name = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        question = request.form['question']
        answer = request.form['answer']

        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('signup'))
        if not validate_password(password):
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('signup'))

        cursor = connection.cursor()
        sql = "INSERT INTO student_register (f_name, l_name, email, question, answer, password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (f_name, l_name, email, question, answer, password)

        try:
            cursor.execute(sql, values)
            connection.commit()
            flash('Registration successful!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {str(err)}', 'error')

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
