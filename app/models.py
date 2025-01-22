from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref=db.backref('folders', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    creator = db.Column(db.String(255), nullable=False)  # Нове поле
    terms = db.Column(db.Integer, default=0)  # Нове поле
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref=db.backref('decks', lazy=True))
    folder = db.relationship('Folder', backref=db.backref('decks', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "creator": self.creator,  # Додано нове поле
            "terms": self.terms,      # Додано нове поле
            "created_at": self.created_at
        }

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    front_title = db.Column(db.String(255), nullable=False)
    back_title = db.Column(db.String(255), nullable=False)
    back_description = db.Column(db.Text, nullable=True)  # Using Text for longer content
    image_url = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_reviewed = db.Column(db.DateTime, nullable=True)
    review_count = db.Column(db.Integer, default=0)
    confidence_level = db.Column(db.Integer, default=0)  # 0-5 scale for spaced repetition
    
    # Relationship with Deck
    deck = db.relationship('Deck', backref=db.backref('flashcards', lazy=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "deck_id": self.deck_id,
            "front_title": self.front_title,
            "back_title": self.back_title,
            "back_description": self.back_description,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "last_reviewed": self.last_reviewed,
            "review_count": self.review_count,
            "confidence_level": self.confidence_level
        }
    
    