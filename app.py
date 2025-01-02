from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="flutter"
)
cursor = db.cursor()


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    try:
        # Insert new user
        cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)",
                       (email, password))
        db.commit()
        return jsonify({'status': 'success', 'message': 'User registered successfully'})
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)})


@app.route('/save_receipt', methods=['POST'])
def save_receipt():
    data = request.json
    receipt_text = data['receipt']

    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO flutter.receipts (receipt_text) VALUES (%s)", (receipt_text,))
        db.commit()
        cursor.close()
        return jsonify({'status': 'success', 'message': 'Receipt saved successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'Failed to save receipt'}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'status': 'success', 'id': user['id']})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
