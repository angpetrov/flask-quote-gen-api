from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash
db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)  # Add this line

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.password_hash = generate_password_hash(password)  # Add this line

    def __repr__(self):
        return f"<User {self.username}>"


class QuoteModel(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(), nullable=False)
    author = db.Column(db.String())
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, quote, author, user_id):
        self.quote = quote
        self.author = author
        self.user_id = user_id

    def __repr__(self):
        return f"<Quote {self.id}>"
