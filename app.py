from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session management

DB_NAME = 'vehicles.db'

# Function to create database if it doesn't exist
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table for vehicles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            owner TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

create_database()

# Function to get language from session (default to 'en')
def get_language():
    return session.get('language', 'en')

# Route to change language
@app.route('/change_language/<lang>')
def change_language(lang):
    if lang in ['en', 'vi']:  # Add more languages if needed
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

# Home page to display vehicles
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()
    lang = get_language()
    return render_template('index.html', vehicles=vehicles, lang=lang)

# Add vehicle
@app.route('/add', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        license_plate = request.form['license_plate']
        vehicle_type = request.form['vehicle_type']
        brand = request.form['brand']
        owner = request.form['owner']
        registration_date = request.form['registration_date']
        phone = request.form['phone']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vehicles (license_plate, vehicle_type, brand, owner, registration_date, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (license_plate, vehicle_type, brand, owner, registration_date, phone))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_vehicle.html')

# Edit vehicle
@app.route('/edit/<int:vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        license_plate = request.form['license_plate']
        vehicle_type = request.form['vehicle_type']
        brand = request.form['brand']
        owner = request.form['owner']
        registration_date = request.form['registration_date']
        phone = request.form['phone']

        cursor.execute('''
            UPDATE vehicles
            SET license_plate = ?, vehicle_type = ?, brand = ?, owner = ?, registration_date = ?, phone = ?
            WHERE id = ?
        ''', (license_plate, vehicle_type, brand, owner, registration_date, phone, vehicle_id))
        conn.commit()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM vehicles WHERE id=?", (vehicle_id,))
    vehicle = cursor.fetchone()
    conn.close()

    return render_template('edit_vehicle.html', vehicle=vehicle)

# Delete vehicle
@app.route('/delete/<int:vehicle_id>', methods=['GET'])
def delete_vehicle(vehicle_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Search vehicle
@app.route('/search', methods=['GET'])
def search_vehicle():
    search_term = request.args.get('query')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE license_plate LIKE ? OR owner LIKE ?", 
                   ('%' + search_term + '%', '%' + search_term + '%'))
    vehicles = cursor.fetchall()
    conn.close()
    lang = get_language()
    return render_template('index.html', vehicles=vehicles, lang=lang)

if __name__ == "__main__":
    app.run(debug=True)
