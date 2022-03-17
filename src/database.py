from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), unique=True, nullable=False)
    email=db.Column(db.String(150), unique=True, nullable=False)
    password=db.Column(db.Text(), nullable=False)    
    created_at=db.Column(db.DateTime(), default=datetime.now())
    updated_at=db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
    