from flask import Blueprint, request, jsonify
from app import db
from app.models import Deck, Flashcard

bp = Blueprint('updateflashcard', __name__, url_prefix='/api')


@bp.route('/update-flashcard/<int:flashcard_id>', methods=['PUT'])
def update_flashcard(flashcard_id):
    data = request.get_json()
    flashcard = Flashcard.query.get(flashcard_id)
    if not flashcard:
        return jsonify({"message": "Flashcard not found"}), 404
    
    print(data)

    '''confidence_mapping = {
        'fail': 1,
        'hard': 2,
        'good': 3,
        'excellent': 4
    }'''

    flashcard.confidence_level = data.get('confidence_level', flashcard.confidence_level)

    print(f"xexe {flashcard.confidence_level}")
    print(f"xexe { data.get('confidence_level', flashcard.confidence_level)}")

    flashcard.next_review = data.get('next_review', flashcard.next_review)
    db.session.commit()

    return jsonify(flashcard.to_dict()), 200