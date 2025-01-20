from flask import Blueprint, jsonify
from app.models import User, Folder, Deck

bp = Blueprint('folder', __name__, url_prefix='/api')

@bp.route('/folders/<int:user_id>', methods=['GET'])
def get_folders_with_decks(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    folders = Folder.query.filter_by(user_id=user_id).all()

    # Формуємо JSON для кожної папки з її колодами
    folder_list = []
    for folder in folders:
        decks_in_folder = Deck.query.filter_by(folder_id=folder.id).all()
        decks_data = [{"id": deck.id, "name": deck.name} for deck in decks_in_folder]
        
        folder_list.append({
            "id": folder.id,
            "name": folder.name,
            "created_at": folder.created_at,
            "decks": decks_data  # Додаємо колоди в папку
        })

    print(folder_list)

    return jsonify(folder_list), 200
