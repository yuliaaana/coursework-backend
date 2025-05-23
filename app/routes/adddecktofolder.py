from flask import Flask, request, jsonify
from flask import Blueprint, request, jsonify
from app import db
from app.models import Deck, Folder

bp = Blueprint('adddeckstofolder', __name__, url_prefix='/api')


@bp.route('/add-deck-to-folder', methods=['POST'])
def add_decks_to_folder():
    try:
        data = request.get_json()

        folder_id = data.get('folderId')
        deck_ids = data.get('deckIds', [])

        if not folder_id or not deck_ids:
            return jsonify({"error": "Missing folderId or deckIds"}), 400

        folder = Folder.query.get(folder_id)
        if not folder:
            return jsonify({"error": "Folder not found"}), 404

        Deck.query.filter(Deck.id.in_(deck_ids)).update({"folder_id": folder_id}, synchronize_session=False)
        db.session.commit()

        return jsonify({"message": "Decks successfully added to folder"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
