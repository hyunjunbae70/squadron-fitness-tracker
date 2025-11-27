Squadron Fitness Tracker

A web application built to replace the Excel-based fitness tracking system used in my squadron. It allows personnel to log workouts, view their progress, and compare performance across the unit. This is a recreation of my original project (in Korean), which was hosted on a local machine.

Key Features:  
User accounts and profiles with session-based authentication  
Workout logging for running, strength training, and bodyweight exercises  
Progress charts using Chart.js  
Squadron leaderboard to encourage friendly competition  
Mobile-friendly interface for quick logging after PT sessions

Tech Stack:  
Backend: Flask (Python), SQLite  
Frontend: HTML/CSS, Bootstrap, JavaScript, Chart.js  
Auth: Sessions with password hashing (Werkzeug)

Exercise Data Tracked:  
Running (time + distance)  
Strength exercises (weight, sets, reps)  
Bodyweight movements  
Squadron PT events

To run project: run 'python app.py' then open http://127.0.0.1:5000/ on browser
