from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref=db.backref('decks', lazy=True))
    folder = db.relationship('Folder', backref=db.backref('decks', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        folders = Folder.query.filter_by(user_id=user.id).all()
        decks = Deck.query.filter_by(user_id=user.id).all()

        folder_list = [{"id": folder.id, "name": folder.name, "created_at": folder.created_at} for folder in folders]
        deck_list = [{"id": deck.id, "name": deck.name, "folder_id": deck.folder_id, "created_at": deck.created_at} for deck in decks]

        return jsonify({
            "message": "Login successful",
            "redirect_url": "/dashboard",
            "user_id": user.id,
            "folders": folder_list,
            "decks": deck_list
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    

@app.route('/api/user-data/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    folders = Folder.query.filter_by(user_id=user_id).all()
    decks = Deck.query.filter_by(user_id=user_id).all()

    folder_list = [folder.to_dict() for folder in folders]
    deck_list = [deck.to_dict() for deck in decks]

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

    print(user_data)

    return jsonify({
        "user": user_data,  
        "folders": folder_list,
        "decks": deck_list
    }), 200

if __name__ == "__main__":
    app.run(debug=True)