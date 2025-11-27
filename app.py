from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production!

# Database setup
def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                  username TEXT UNIQUE, 
                  password TEXT,
                  rank TEXT,
                  squadron TEXT)''')
    
    # Workouts table
    c.execute('''CREATE TABLE IF NOT EXISTS workouts
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  exercise_type TEXT,
                  duration INTEGER,
                  distance REAL,
                  reps INTEGER,
                  weight REAL,
                  date TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Simple dashboard - you can expand this later
    return render_template('dashboard.html', username=session.get('username'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
