from flask import Blueprint, request, jsonify
from app import db
from app.models import Folder, Deck

bp = Blueprint('createfolder', __name__, url_prefix='/api')

# Ендпойнт для створення папки
@bp.route('/create-folder', methods=['POST'])
def create_folder():
    data = request.json

    # Перевірка необхідних даних
    user_id = data.get('user_id')
    if not user_id or not data.get('name') or not data.get('decks'):
        return jsonify({"message": "User ID, Name and Decks are required"}), 400

    folder_name = data.get('name')
    deck_ids = data.get('decks')  # Очікуємо список id деків

    # Створення нової папки
    new_folder = Folder(name=folder_name, user_id=user_id)
    db.session.add(new_folder)
    db.session.commit()

    # Виведення в консоль отриманих деків
    print("Selected decks:", deck_ids)

    # Повернення успішної відповіді
    return jsonify({
        "message": "Folder created successfully",
        "folder": new_folder.to_dict(),
        "decks": deck_ids
    }), 201
