import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ola_app"
    )

def verify_user(phoneno, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE phoneno=%s AND password=%s", (phoneno, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def add_user(username, phoneno, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, phoneno, password) VALUES (%s, %s, %s)", (username, phoneno, password))
        conn.commit()
        success = True
    except mysql.connector.IntegrityError:
        success = False
    conn.close()
    return success

def book_ride(current_user_id, pickup, dropoff):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rides (user_id, pickup, dropoff) VALUES (%s, %s, %s)", (current_user_id, pickup, dropoff))
    ride_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ride_id

def process_payment(ride_id, payment_method, amount):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (ride_id, payment_method, amount) VALUES (%s, %s, %s)", (ride_id, payment_method, amount))
    conn.commit()
    conn.close()
    return True

def submit_feedback(ride_id, rating, comments):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (ride_id, rating, comments) VALUES (%s, %s, %s)", (ride_id, rating, comments))
    conn.commit()
    conn.close()
    return True
