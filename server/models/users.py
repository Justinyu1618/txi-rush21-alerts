from server import db
from flask import Flask

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50), unique=True)
    active = db.Column(db.Boolean, default=True)

    def populate(self, data, **kwargs):
        for key, val in data.items():
            if hasattr(self, key): setattr(self, key, val)
        for key, val in kwargs.items():
            if hasattr(self, key): setattr(self, key, val)
        
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}