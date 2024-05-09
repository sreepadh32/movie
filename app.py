from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="movie_booking"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect('/movies')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

# Movies page
@app.route('/movies')
def movies():
    # Fetch all movies from the database
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    return render_template('movies.html', movies=movies)

# Theatre page
@app.route('/theatres/<movie_id>')
def theatres(movie_id):
    # Fetch all theatres for the selected movie from the database
    cursor.execute("SELECT * FROM theatres WHERE movie_id = %s", (movie_id,))
    theatres = cursor.fetchall()

    return render_template('theatres.html', theatres=theatres)

# Seats page
@app.route('/seats/<theatre_id>')
def seats(theatre_id):
    # Fetch all available seats for the selected theatre from the database
    cursor.execute("SELECT * FROM seats WHERE theatre_id = %s AND is_booked = 0", (theatre_id,))
    seats = cursor.fetchall()

    return render_template('seats.html', seats=seats)

# Booking confirmation pagel
@app.route('/confirm/<seat_id>')
def confirm(seat_id):
    # Update the selected seat as booked in the database
    cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = %s;", (seat_id,))
    db.commit()

    return render_template('confirm.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)