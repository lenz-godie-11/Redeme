import re
import secrets
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db  # Look upward to grab your connection tool

# Establish the blueprint package
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def signup():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password are required?'}), 400

    username = username.strip()

    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'username must be 3-20 characters long'}), 400

    if len(password) < 12:
        return jsonify({'error': 'Password must be at least 12 characters long'}), 400

    if not re.match("^[a-zA-Z0-9_]+$", username):
        return jsonify({'error': 'Username can only have letters, numbers, and underscores'}), 400

    conn = get_db()
    existing_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    if existing_user:
        conn.close()
        return jsonify({'error': 'Username already taken'}), 409 

    password_hash = generate_password_hash(password)
    token = secrets.token_hex(24)

    conn.execute(
        'INSERT INTO users (username, password_hash, token) VALUES (?, ?, ?)',
        (username, password_hash, token)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Signup successful!', 'token': token}), 201 

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = get_db()
    user = conn.execute(
        'SELECT password_hash, token FROM users WHERE username = ?', 
        (username,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid username or password'}), 401 

    return jsonify({'message': 'Login successful!', 'token': user['token']}), 200
