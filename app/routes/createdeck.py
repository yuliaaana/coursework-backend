from flask import Blueprint, request, jsonify
from app import db
from app.models import Deck, Flashcard

bp = Blueprint('create_deck', __name__, url_prefix='/api')

@bp.route('/create-deck', methods=['POST'])
def create_deck():
    data = request.json

    user_id = data.get('user_id')
    deck_name = data.get('name')
    flashcards = data.get('flashcards')

    if not user_id or not deck_name:
        return jsonify({"message": "User ID and Deck Name are required"}), 400

    if not flashcards or not any(card.get('front') and card.get('back') for card in flashcards):
        return jsonify({"message": "At least one valid flashcard is required"}), 400

    new_deck = Deck(
        user_id=user_id,
        name=deck_name,
        creator="Unknown Creator", ###############################
        terms=len(flashcards)
    )
    db.session.add(new_deck)
    db.session.commit()

    for card in flashcards:
        if card.get('front') and card.get('back'):
            new_flashcard = Flashcard(
                deck_id=new_deck.id,
                front_title=card['front'],
                back_title=card['back'],
                back_description=card.get('description', ""),
                image_url=card.get('image_url', None)  
            )
            db.session.add(new_flashcard)

    db.session.commit()

    return jsonify({
        "message": "Deck created successfully",
        "deck": new_deck.to_dict(),
        "flashcards": [card.to_dict() for card in new_deck.flashcards]
    }), 201
