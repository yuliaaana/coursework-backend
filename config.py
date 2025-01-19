import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1234@localhost/flashcardsapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
