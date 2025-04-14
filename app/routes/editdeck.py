from flask import Blueprint, request, jsonify
from app.models import db, Deck, Flashcard

bp = Blueprint('update-deck', __name__, url_prefix='/api')

'''@bp.route('/update-deck/<int:deck_id>', methods=['PUT'])
def update_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({"message": "Deck not found"}), 404

    data = request.get_json()
    deck.name = data.get('name', deck.name)
    deck.is_public = data.get('is_public', deck.is_public)

    new_cards = data.get('new_flashcards', [])
    for card_data in new_cards:
        card = Flashcard(
            deck_id=deck.id,
            front_title=card_data['front_title'],
            back_title=card_data['back_title'],
            back_description=card_data.get('back_description'),
            image_url=card_data.get('image_url')
        )
        db.session.add(card)
        deck.terms += 1  # оновлюємо лічильник карток

    db.session.commit()
    
    return jsonify({
        "message": "Deck updated successfully",
        "deck": deck.to_dict()
    }), 200'''
@bp.route('/update-deck/<int:deck_id>', methods=['PUT'])
def update_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({"message": "Deck not found"}), 404

    data = request.get_json()
    deck.name = data.get('name', deck.name)
    deck.is_public = data.get('is_public', deck.is_public)

    # Видалити всі старі картки
    Flashcard.query.filter_by(deck_id=deck.id).delete()
    deck.terms = 0  # Скидаємо лічильник

    # Додати нові картки
    new_cards = data.get('new_flashcards', [])
    for card_data in new_cards:
        card = Flashcard(
            deck_id=deck.id,
            front_title=card_data['front_title'],
            back_title=card_data['back_title'],
            back_description=card_data.get('back_description'),
            image_url=card_data.get('image_url')
        )
        db.session.add(card)
        deck.terms += 1

    db.session.commit()
    
    return jsonify({
        "message": "Deck updated successfully",
        "deck": deck.to_dict()
    }), 200

