from flask import Blueprint, request, jsonify
from app.models import User, Folder, Deck
from app import bcrypt, db

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        folders = Folder.query.filter_by(user_id=user.id).all()
        decks = Deck.query.filter_by(user_id=user.id).all()

        folder_list = [folder.to_dict() for folder in folders]
        deck_list = [
            {
                "id": deck.id,
                "name": deck.name,
                "creator": deck.creator,  # Додано
                "terms": deck.terms,      # Додано
                "folder_id": deck.folder_id,
                "created_at": deck.created_at
            }
            for deck in decks
        ]

        return jsonify({
            "message": "Login successful",
            "redirect_url": "/dashboard",
            "user_id": user.id,
            "folders": folder_list,
            "decks": deck_list
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
