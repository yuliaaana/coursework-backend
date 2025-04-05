from flask import Blueprint, jsonify
from app.models import User, Folder

bp = Blueprint('folders', __name__, url_prefix='/api')

@bp.route('/folders/<int:user_id>', methods=['GET'])
def get_folders_with_decks(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    folders = Folder.query.filter_by(user_id=user_id).all()
    print(folders)
    folder_list = []
    for folder in folders:
        decks_data = [{"id": deck.id, "name": deck.name} for deck in folder.decks]
        folder_list.append({
            "id": folder.id,
            "name": folder.name,
            "created_at": folder.created_at.isoformat(),  
            "decks": decks_data
        })

    return jsonify(folder_list), 200
