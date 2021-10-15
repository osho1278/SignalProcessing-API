import datetime
from . import db
from sqlalchemy import ForeignKey


class WidgetsModel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    category = db.Column(db.String(100))
    function_type = db.Column(db.String(100))
    data = db.Column(db.PickleType)
    createdBy = db.Column(db.Integer, ForeignKey('user.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, category, label, data,function_type,createdBy):
        self.category = category
        self.label = label
        self.data = data
        self.function_type = function_type
        self.createdBy = createdBy
        # self.date_joined = pin
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}