import base64
from flask import Blueprint, jsonify
from app.models import User, Folder, Deck
import os

bp = Blueprint('user', __name__, url_prefix='/api')

# Ендпойнт отримання даних користувача
@bp.route('/user-data/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Retrieve user's folders and decks
    folders = Folder.query.filter_by(user_id=user_id).all()
    decks = Deck.query.filter_by(user_id=user_id).all()

    folder_list = [folder.to_dict() for folder in folders]
    deck_list = [
        {
            "id": deck.id,
            "name": deck.name,
            "creator": deck.user.username, 
            "terms": deck.terms,     
            "folder_id": deck.folder_id,
            "created_at": deck.created_at
        }
        for deck in decks
    ]

    # Convert avatar to base64 if an avatar exists
    avatar_base64 = None
    if user.avatar:
        try:
            avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')  # Перетворюємо бінарні дані в base64
        except Exception as e:
            print("Error encoding avatar:", e)
            avatar_base64 = None

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": avatar_base64  # Повертаємо base64-encoded аватар
    }

    return jsonify({
        "user": user_data,
        "folders": folder_list,
        "decks": deck_list
    }), 200
