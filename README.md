# Squadron Fitness Tracker

A fitness tracking web app I built during military service to replace Excel spreadsheets for squadron PT tracking. Increased participation by 40% through leaderboards and progress charts.

*Note: This is a rewrite of the original Korean version I deployed while serving.*

## What It Does

Tracks workouts for military personnel with competitive leaderboards and progress visualisation. Users log exercises (running, strength training, bodyweight), view their stats over time, and compete on team/individual leaderboards.

## Features

### User Authentication & Profiles
- Secure user registration and login with password hashing
- Session-based authentication
- User profiles with rank and squadron information
- Protected routes for authenticated users only

### Workout Logging
- Comprehensive workout entry system supporting:
  - **Running**: Track duration and distance
  - **Strength Training**: Log weight, reps, and sets
  - **Bodyweight Exercises**: Record reps and duration
  - **Custom Exercise Types**: Flexible logging for any activity
- Date tracking with automatic timestamp support
- Recent workout history display

### Progress Visualization
- **Weekly Activity Charts**: Visual representation of workouts over the past 7 days
- **Exercise Type Distribution**: Pie/bar charts showing workout variety
- Interactive charts powered by Chart.js
- Real-time data updates

### Competitive Leaderboards
- Multiple leaderboard views:
  - **All-Time**: Overall performance rankings
  - **Weekly**: Current week's top performers
  - **Monthly**: 30-day performance metrics
  - **Squadron-Specific**: Filter by squadron for team competition
- Multiple ranking metrics:
  - Total workouts completed
  - Total distance covered
  - Total duration
- Personal position tracking

### Responsive Design
- Mobile-friendly interface using Bootstrap
- Optimized for quick logging after PT sessions
- Cross-device compatibility

## Tech Stack

### Backend
- **Flask** (Python) - Web framework
- **SQLite** - Lightweight database
- **Werkzeug** - Password hashing and security utilities

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript** - Interactive functionality
- **Chart.js** - Data visualization library

### Security
- Password hashing using Werkzeug's security utilities
- Session-based authentication
- SQL injection protection through parameterized queries

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd squadron-fitness-tracker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database**
   The database will be automatically created when you first run the application. Alternatively, you can manually initialize it:
   ```bash
   python database/init_db.py
   ```

6. **Set environment variable** (optional, for production)
   ```bash
   export FLASK_SECRET="your-secret-key-here"
   ```
   On Windows:
   ```powershell
   $env:FLASK_SECRET="your-secret-key-here"
   ```

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. **Register a new account**
   - Click "Register" on the homepage
   - Fill in username, password, rank, and squadron (optional)
   - Minimum password length: 8 characters

4. **Log in**
   - Use your credentials to access the dashboard

5. **Log workouts**
   - Navigate to the dashboard
   - Fill in the workout form with exercise details
   - View your progress charts and recent activity

6. **View leaderboards**
   - Access the leaderboard page
   - Filter by time period (all-time, week, month, squadron)
   - Switch between different metrics (workouts, distance, duration)

7. **View profile**
   - Check your account information and registration date

## Project Structure

```
squadron-fitness-tracker/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── fitness.db            # SQLite database (created on first run)
│
├── database/
│   └── init_db.py        # Database initialization script
│
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard with charts
│   ├── leaderboard.html  # Leaderboard page
│   └── profile.html      # User profile page
│
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Custom styles
│   ├── js/
│   │   └── charts.js    # Chart.js configuration
│   └── images/          # Image assets
│
└── utils/
    └── helpers.py       # Utility functions
```

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `password_hash` - Hashed password
- `rank` - User's rank (optional)
- `squadron` - Squadron assignment (optional)
- `created_at` - Account creation timestamp

### Workouts Table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `exercise_type` - Type of exercise
- `duration` - Duration in minutes (optional)
- `distance` - Distance in miles (optional)
- `reps` - Number of repetitions (optional)
- `weight` - Weight in pounds (optional)
- `date` - Workout date

## Security Notes

- Passwords are hashed using Werkzeug's secure password hashing
- SQL injection protection through parameterized queries
- Session-based authentication prevents unauthorized access
- **Important**: Change the `FLASK_SECRET` environment variable in production environments
