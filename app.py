from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "your-secret-key-here")  # change in production!

DATABASE = "fitness.db"

# -----------------------
# Database helpers
# -----------------------
def get_db(conn_path=DATABASE):
    conn = sqlite3.connect(conn_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users table (store hashed passwords)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rank TEXT,
            squadron TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Workouts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exercise_type TEXT,
            duration INTEGER,
            distance REAL,
            reps INTEGER,
            weight REAL,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# -----------------------
# Auth utilities
# -----------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# -----------------------
# Routes
# -----------------------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        rank = request.form.get("rank", "").strip()
        squadron = request.form.get("squadron", "").strip()

        if not username or not password:
            flash("Username and password are required.", "warning")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "warning")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            conn = get_db()
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password_hash, rank, squadron) VALUES (?, ?, ?, ?)",
                (username, password_hash, rank or None, squadron or None),
            )
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            flash("Username already taken. Choose another one.", "danger")
            return render_template("register.html")

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Provide username and password.", "warning")
            return render_template("login.html")

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session.get("user_id")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM workouts WHERE user_id = ? ORDER BY date(date) DESC LIMIT 10",
        (user_id,),
    )
    recent = c.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        recent_workouts=recent,
    )


@app.route("/workouts/log", methods=["POST"])
@login_required
def log_workout():
    exercise_type = request.form.get("exercise_type", "").strip()
    date_str = request.form.get("date") or ""
    duration = request.form.get("duration")
    distance = request.form.get("distance")
    reps = request.form.get("reps")
    weight = request.form.get("weight")

    if not exercise_type:
        flash("Exercise type is required.", "warning")
        return redirect(url_for("dashboard"))

    if not date_str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

    # Normalize numeric fields, allow blanks to stay NULL
    def to_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def to_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    duration_val = to_int(duration)
    reps_val = to_int(reps)
    distance_val = to_float(distance)
    weight_val = to_float(weight)

    conn = get_db()
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO workouts (user_id, exercise_type, duration, distance, reps, weight, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session["user_id"],
            exercise_type,
            duration_val,
            distance_val,
            reps_val,
            weight_val,
            date_str,
        ),
    )
    conn.commit()
    conn.close()

    flash("Workout logged!", "success")
    return redirect(url_for("dashboard"))


# -----------------------
# Optional: simple profile route
# -----------------------
@app.route("/profile")
@login_required
def profile():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, username, rank, squadron, created_at FROM users WHERE id = ?", (session["user_id"],))
    user = c.fetchone()
    conn.close()
    user_data = dict(user) if user else None
    return render_template("profile.html", user=user_data)


# -----------------------
# App startup
# -----------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
