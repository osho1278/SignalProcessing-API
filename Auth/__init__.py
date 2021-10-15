
# flask imports
from flask import Flask, request, jsonify, make_response
# from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
import jwt
from datetime import datetime, timedelta
from functools import wraps
import json
# app.config['SECRET_KEY'] = 'your secret key'

class Authenticator:
    def token_required(self,f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            # return 401 if token is not passed
            if not token:
                return jsonify({'message' : 'Token is missing , please add token !!'}), 401
    
            try:
                print(token)
                tt=token.split(" ")[1]
                # decoding the payload to fetch the stored details
                data = jwt.decode(tt, 'SECRET_KEY',algorithms=["HS256"])
                print(data)
                current_user = data
            except Exception as e:
                print(e)
                return jsonify({
                    'message' : 'Token is invalid !!'
                }), 401
            # returns the current logged in users contex to the routes
            return  f(current_user, *args, **kwargs)
        return decorated
  