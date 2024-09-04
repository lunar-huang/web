from flask import Flask, render_template, request, redirect, url_for, session, flash
import mariadb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to establish a connection to MariaDB
def get_db_connection():
    conn = mariadb.connect(
        user="root",  # Your MariaDB username
        password="root",  # Your MariaDB password
        host="localhost",
        database="user_record"  # The database you created
    )
    return conn

# Route for the homepage (index)
@app.route('/')
def home():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute query to retrieve all usernames
        cursor.execute('SELECT username FROM users')
        usernames = cursor.fetchall()  # Fetch all rows
        
        conn.close()  # Always close the connection
        
        # Render the index.html template, passing the usernames to the template
        return render_template('index.html', usernames=usernames)
    
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return "Error connecting to the database", 500

# Login and other routes go here...

if __name__ == '__main__':
    app.run(debug=True)
