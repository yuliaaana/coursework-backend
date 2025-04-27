import base64
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash
import os

bp = Blueprint('profile', __name__, url_prefix='/api')

# Ендпойнт отримання даних користувача
@bp.route('/user-data/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user = User.query.get(user_id)
    if user:
        # Encode avatar to base64 if it exists
        avatar_base64 = None
        if user.avatar:
            avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')
        
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar": avatar_base64  # Sending avatar as base64 encoded string
            }
        })
    else:
        return jsonify({"error": "User not found"}), 404

# Ендпойнт оновлення даних користувача
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

    # Encode avatar to base64 if it exists
    avatar_base64 = None
    if user.avatar:
        avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')

    db.session.commit()

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": avatar_base64  # Sending avatar as base64 encoded string
        }
    })

# Ендпойнт зміни пароля
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

# Ендпойнт завантаження аватара
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

    # Read the file as binary data
    try:
        avatar_data = file.read()
        # Save the binary data in the database
        user.avatar = avatar_data
        db.session.commit()

        # After successfully uploading, we return the new avatar in Base64
        avatar_base64 = base64.b64encode(avatar_data).decode('utf-8')

        return jsonify({
            "message": "Avatar uploaded successfully",
            "avatar": avatar_base64  # Sending the uploaded avatar as base64 string
        })
    except Exception as e:
        print("Error processing file:", str(e))
        return jsonify({"error": str(e)}), 500
