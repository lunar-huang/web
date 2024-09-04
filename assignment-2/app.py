from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 session 加密，换成更安全的密钥

# 首页路由
@app.route('/')
def home():
    return render_template('index.html')  # 默认显示登录页面

# 数据库连接
def get_db_connection():
    conn = mariadb.connect(
        user="root",
        password="yourpassword",  # 替换为你的 MariaDB 密码
        host="localhost",
        database="user_system"
    )
    return conn
""" 
# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)  # 对密码进行加密

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
            conn.close()
            flash('注册成功，请登录', 'success')  # 提示用户注册成功
            return redirect(url_for('login'))
        except mariadb.Error as e:
            flash(f'Error: {e}', 'danger')
    
    return render_template('register.html')  # 渲染注册页面

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):  # 验证用户输入的密码是否匹配
            session['user'] = username  # 创建 session
            flash('登录成功', 'success')
            return redirect(url_for('dashboard'))  # 跳转到用户主页或其他功能页
        else:
            flash('用户名或密码错误', 'danger')

    return render_template('login.html')  # 渲染登录页面

# 用户主页（示例）
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        flash('请先登录', 'warning')
        return redirect(url_for('login'))

# 注销路由（可选）
@app.route('/logout')
def logout():
    session.pop('user', None)  # 清除 session
    flash('已注销', 'info')
    return redirect(url_for('login')) """

if __name__ == '__main__':
    app.run(debug=True)
