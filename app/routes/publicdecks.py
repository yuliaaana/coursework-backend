from flask import Blueprint, jsonify
from app.models import Deck

bp = Blueprint('publicdecks', __name__, url_prefix='/api')

@bp.route('/public-decks/<int:user_id>', methods=['GET'])
def get_public_decks(user_id):
    public_decks = Deck.query.filter(
        Deck.is_public == True,
        Deck.user_id != user_id
    ).all()

    deck_list = [
        {
            "id": deck.id,
            "name": deck.name,
            "creator": deck.user.username, 
            "creator_id": deck.user.id, 
            "terms": deck.terms,
            "created_at": deck.created_at,
            "is_public": deck.is_public
        }
        for deck in public_decks
    ]

    return jsonify({
        "public_decks": deck_list
    }), 200
