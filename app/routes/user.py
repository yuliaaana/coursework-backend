from flask import Blueprint, jsonify
from app.models import User, Folder, Deck

bp = Blueprint('user', __name__, url_prefix='/api')

@bp.route('/user-data/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    #folders = Folder.query.filter_by(user_id=user_id).all()
    #decks = Deck.query.filter_by(user_id=user_id).all()

    folders = Folder.query.filter_by(user_id=user_id).all()
    decks = Deck.query.filter_by(user_id=user_id).all()

    folder_list = [folder.to_dict() for folder in folders]
    deck_list = [
        {
            "id": deck.id,
            "name": deck.name,
            "creator": deck.creator,  
            "terms": deck.terms,     
            "folder_id": deck.folder_id,
            "created_at": deck.created_at
        }
        for deck in decks
    ]

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

    return jsonify({
        "user": user_data,
        "folders": folder_list,
        "decks": deck_list
    }), 200
