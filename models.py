from extensions import db  # Import the centralized SQLAlchemy instance
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

# GuestType Model
class GuestType(db.Model):
    __tablename__ = 'guest_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship to Guest
    guests = db.relationship('Guest', back_populates='type', lazy='dynamic')

    def __repr__(self):
        return f"<GuestType {self.name}>"

# Guest Model
class Guest(db.Model):
    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    guest_type_id = db.Column(db.Integer, db.ForeignKey('guest_type.id'), nullable=False)

    # Relationship to GuestType
    type = db.relationship('GuestType', back_populates='guests')

    def __repr__(self):
        return f"<Guest {self.name}>"

# User Model (for authentication and roles)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='User', nullable=False)  # e.g., 'Admin', 'Moderator', 'User'

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"