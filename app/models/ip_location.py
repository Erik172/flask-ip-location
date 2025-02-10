from app import db

class IPLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))
    loc = db.Column(db.String(50))

    def __repr__(self):
        return f'<IPLocation {self.ip}>'