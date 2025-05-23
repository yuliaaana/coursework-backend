import base64
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash
import os

bp = Blueprint('profile', __name__, url_prefix='/api')

@bp.route('/user-data/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user = User.query.get(user_id)
    if user:
        avatar_base64 = None
        if user.avatar:
            avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')
        
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar": avatar_base64  
            }
        })
    else:
        return jsonify({"error": "User not found"}), 404

@bp.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if username:
        user.username = username
    if email:
        user.email = email

    avatar_base64 = None
    if user.avatar:
        avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')

    db.session.commit()

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": avatar_base64
        }
    })

@bp.route('/change-password/<int:user_id>', methods=['PUT'])
def change_password(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({"error": "Password is required"}), 400

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully"})

@bp.route('/upload-avatar/<int:user_id>', methods=['POST'])
def upload_avatar(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    print("Files in request:", request.files)
    
    if 'avatar' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        avatar_data = file.read()

        user.avatar = avatar_data
        db.session.commit()

        avatar_base64 = base64.b64encode(avatar_data).decode('utf-8')

        return jsonify({
            "message": "Avatar uploaded successfully",
            "avatar": avatar_base64 
        })
    except Exception as e:
        print("Error processing file:", str(e))
        return jsonify({"error": str(e)}), 500
