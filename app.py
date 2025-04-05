from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)