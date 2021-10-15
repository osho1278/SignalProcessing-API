import datetime
from . import db
from sqlalchemy import ForeignKey


class OutputModel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    output = db.Column(db.PickleType)
    createdBy = db.Column(db.Integer, ForeignKey('user.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, output, createdBy):
        self.name = name
        self.output = output
        self.createdBy = createdBy
        # self.date_joined = pin
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}