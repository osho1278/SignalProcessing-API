from flask import Flask, request,redirect,jsonify, url_for,make_response
from datetime import datetime, timedelta
import jwt
from Models.user import User,db
from sqlalchemy import and_,select

class Login:
    def __init__(self, app):
        self.app = app

    def add_route(self):
        @self.app.route('/login', methods=['POST'])
        def Login():
            auth = request.json
            print("Request is ",auth)
            if not auth or not auth.get('username') or not auth.get('password'):
                # returns 401 if any email or / and password is missing
                return make_response(
                    'Could not verify',
                    401,
                    {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
                )
            if True: #check_password_hash(user.password, auth.get('password')):
                # generates the JWT Token
                # result=User.query.filter(and_(User.username==auth.get('username'),User.password==auth.get('password')))

                query = select([User]).where(User.username==auth.get('username'),User.password==auth.get('password'))
                result=db.session.execute(query)
                print("-----------",result)
                id,name=None,None
                for row in result:
                    print(row.User.serialized)
                    id=row.User.id
                    name=row.User.username
                    print("id= ",id," and name= ",name)
                if(not name):
                    return make_response('Invalid username or password',   403,    {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'})

                token = jwt.encode({
                    'id': id,
                    'name':name,
                    'exp': datetime.utcnow() + timedelta(minutes=300000)
                }, 'SECRET_KEY',algorithm="HS256")

                return make_response(token, 201)
            # returns 403 if password is wrong
            return make_response(
                'Could not verify',
                403,
                {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
            )
