from flask import Blueprint, request, jsonify
from app import db
from app.models import Deck, Flashcard

bp = Blueprint('deck', __name__, url_prefix='/api')

@bp.route('/deck/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    # Отримання дека з бази даних

    print(deck_id)
    deck = Deck.query.get(deck_id)

    if not deck:
        return jsonify({"message": "Deck not found"}), 404

    # Отримання флешкарток, пов'язаних із деком
    flashcards = Flashcard.query.filter_by(deck_id=deck.id).all()

    # Підготовка відповіді
    print(deck.to_dict())

    return jsonify({
        "deck": deck.to_dict(),
        "flashcards": [card.to_dict() for card in flashcards]  # Додаємо всі флешкарти
    }), 200
