from flask import Blueprint, request, jsonify
from models import get_db

appointments_bp = Blueprint('appointments', __name__)


def get_user_from_token(token):
    conn = get_db()
    user = conn.execute(
        'SELECT id, username FROM users WHERE token = ?', 
        (token,)
    ).fetchone()
    conn.close()
    return user

@appointments_bp.route('/api/appointments', methods=['POST'])
def create_appointment():
    
    
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = get_user_from_token(token)
    
    
    if not user:
        return jsonify({'error': 'Unauthorized. Please log in first.'}), 401

    
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    message = data.get('message', '') 

    
    if not name or not email or not date:
        return jsonify({'error': 'Name, email, and date are required fields'}), 400

    
    conn = get_db()
    conn.execute(
        'INSERT INTO appointment (user_id, name, email, date, message) VALUES (?, ?, ?, ?, ?)',
        (user['id'], name, email, date, message)
    )
    conn.commit()
    conn.close()

    
    return jsonify({'success': True, 'message': 'Appointment booked successfully!'}), 201


@appointments_bp.route('/api/appointments', methods=['GET'])
def get_my_appointments():
    # 1. SECURITY CHECK (Just like your POST route)
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = get_user_from_token(token)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    # 2. DATABASE QUERY
    conn = get_db()
    # Fetch all records for this specific user_id
    # Using fetchall() returns a list of all matching rows
    appointments = conn.execute(
        'SELECT id, name, email, date, message FROM appointment WHERE user_id = ?', 
        (user['id'],)
    ).fetchall()
    conn.close()

    # 3. FORMAT AS JSON
    # Because we use sqlite3.Row, we can convert each row to a dictionary easily
    results = [dict(row) for row in appointments]
    
    return jsonify(results), 200



@appointments_bp.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    # 1. SECURITY CHECK (Identify user by token)
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = get_user_from_token(token)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    # 2. DATABASE DELETE
    conn = get_db()
    # Security: Only delete if BOTH the appointment ID matches AND it belongs to this user
    cursor = conn.execute(
        'DELETE FROM appointment WHERE id = ? AND user_id = ?', 
        (appointment_id, user['id'])
    )
    conn.commit()
    
    # Check if a row was actually deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Appointment not found or unauthorized'}), 404
        
    conn.close()
    return jsonify({'success': True, 'message': 'Appointment cancelled successfully'}), 200
