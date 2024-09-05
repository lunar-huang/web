from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

import mariadb

app = Flask(__name__)
app.secret_key = os.urandom(32)  # Replace with your own secret key
# 设置 session 过期时间为 3 分钟
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

# Database connection setup
# Function to establish a connection to MariaDB
def get_db_connection():
    conn = mariadb.connect(
        user="root",  # Your MariaDB username
        password="root",  # Your MariaDB password
        host="localhost",
        database="user_record"  # The database you created
    )
    return conn

# Home page (index)
@app.route('/')
def home():
    session.permanent = True  # 将 session 设置为永久的，这样可以使用 PERMANENT_SESSION_LIFETIME
     # 尝试连接数据库
    try:
        conn = get_db_connection()
        conn.close()
        connection_status = "Website is ready!"
    except mariadb.Error as e:
        connection_status = f"Failed to connect to the database: {e}"

    return render_template('index.html', connection_status=connection_status)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)  # Hash the password for security
        print(f"Received login request: username={username}, password={password}")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Insert the new user into the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
            conn.commit()
            conn.close()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('home'))
        except mariadb.Error as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('register'))  # Redirect back to register in case of error

    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['user'] = username  # 确保在登录成功后将用户名存储到 session 中
            session.permanent = True  # 设置 session 为永久，使用配置的过期时间
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('home'))
    except mariadb.Error as e:
        flash(f'Database error: {e}', 'danger')
        return redirect(url_for('home'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' in session:  # 检查 session 中是否有用户名
        username = session['user']  # 获取当前登录的用户名
        return render_template('dashboard.html', username=username)  # 将用户名传递给模板
    else:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('home'))  # 如果没有登录，重定向到登录页面


if __name__ == '__main__':
    app.run(debug=True)
