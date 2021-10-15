import datetime
from . import db
from sqlalchemy import ForeignKey


class GraphModel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    graph = db.Column(db.PickleType)
    name = db.Column(db.String(100))
    createdBy = db.Column(db.Integer, ForeignKey('user.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, graph, createdBy):
        self.name = name
        self.graph = graph
        self.createdBy = createdBy
        # self.date_joined = pin
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}