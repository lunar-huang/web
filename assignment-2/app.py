from flask import Flask, request, render_template, flash, redirect, url_for, session, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
import hashlib
import uuid  # 添加这一行来导入 uuid 模块
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
        # 检查用户是否已经登录
    if 'user' in session:
        print(f"User {session['user']} is already logged in. Redirecting to dashboard.")
        return redirect(url_for('dashboard'))
    print("User is not logged in. Staying on the index page.")
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

""" # Login route
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
 """
 
# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    remember_me = request.form.get('remember_me')  # 检查是否勾选了 Remember Me

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            session['user'] = username  # 确保在登录成功后将用户名存储到 session 中
            session.permanent = True  # 设置 session 为永久，使用配置的过期时间

            # 创建响应对象
            response = make_response(redirect(url_for('dashboard')))

            # 如果用户勾选了 "Remember Me"，将 session_id 存储到 cookies 中，并设置 30 天的过期时间
            if remember_me:
                session_id = str(uuid.uuid4())  # 生成一个唯一的 session ID
                session['session_id'] = session_id  # 将 session_id 保存在 session 中
                
                # 存储 session_id 到数据库中
                cursor.execute("UPDATE users SET session_id = ? WHERE id = ?", (session_id, user[0]))
                conn.commit()

                # 将 session_id 设置到 cookies 中，过期时间为 30 天
                response.set_cookie('session_id', session_id, max_age=30*24*60*60)

            conn.close()
            return response
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('home'))
    except mariadb.Error as e:
        flash(f'Database error: {e}', 'danger')
        return redirect(url_for('home'))
    
""" @app.before_request
def load_session_from_cookie():
    print("activate checking session from cookie.")
    session_id = request.cookies.get('session_id')
    
    if session_id and 'user' not in session:
        try:
            # 从数据库中查找 session_id 对应的用户
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE session_id = ?", (session_id,))
            user = cursor.fetchone()
            conn.close()

            if user:
                # 恢复 session，将用户名存储到 session 中
                session['user'] = user[0]                
                # 重定向到个人页面
                print(f"redirect to dashboard for {user[0]}.")
                return redirect(url_for('dashboard'))
            
        except mariadb.Error as e:
            print(f"Database error occurred: {e}")
            
    else:
        print("no session in cookie found. stay in homepage.") """
        
@app.before_request
def load_session_from_cookie():
    print("activate checking session from cookie.")
    session_id = request.cookies.get('session_id')
    
    if session_id:
        print(f"Session ID found in cookie: {session_id}")
    else:
        print("No session ID found in cookie.")
    
    # 检查 session 中是否有 'user'
    if session_id and 'user' not in session:
        print("No user in session, attempting to restore session from database.")
        try:
            # 从数据库中查找 session_id 对应的用户
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE session_id = ?", (session_id,))
            user = cursor.fetchone()
            conn.close()

            if user:
                # 恢复 session，将用户名存储到 session 中
                session['user'] = user[0]                
                print(f"Session restored. Redirecting to dashboard for {user[0]}.")
                
                # 成功恢复会话后，重定向到 dashboard
                return redirect(url_for('dashboard'))
            else:
                print(f"No user found for session ID: {session_id}")
            
        except mariadb.Error as e:
            print(f"Database error occurred: {e}")
            
    elif 'user' in session:
        print(f"User already in session: {session['user']}.")
    else:
        print("No session ID in cookie and no user in session. Stay on the current page.")

    # 如果没有 session 或未恢复，继续处理当前请求，不返回任何内容
    return None



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
