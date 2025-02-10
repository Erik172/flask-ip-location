from datetime import datetime
from app import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(100), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_visited = db.Column(db.DateTime)

    def __repr__(self):
        return f'<URL {self.short_url}>'