import datetime
from . import db

class User(db.Model):
    __table_args__ = (db.UniqueConstraint('id')),
    id = db.Column( db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    username = db.Column(db.String(200),primary_key=True)
    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean,default=True)
    is_staff = db.Column(db.Boolean,default=False)
    is_superuser = db.Column(db.Boolean,default=False)
    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username
        # self.date_joined = pin
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        # return {
        #     'id': self.id,
        #     'name':self.username,     
        # }