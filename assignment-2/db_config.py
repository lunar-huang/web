# db_config.py

class Config:
    # MariaDB配置
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # 替换为你的数据库用户名
    MYSQL_PASSWORD = 'root'  # 替换为你的数据库密码
    MYSQL_DB = 'user_record'

    # Flask-Session配置
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'your_secret_key'  # 请替换为一个强随机密钥
