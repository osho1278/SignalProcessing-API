from flask import Flask, request,redirect,jsonify, url_for,make_response
from datetime import datetime, timedelta
import jwt
from Models.user import User,db

class Signup:
    
    def __init__(self, app):
        self.app = app
        # db.init_app(app)

    def add_route(self):
        @self.app.route('/signup', methods=['POST'])
        def Signup():
            user_details = request.json
            # print(auth)
            if not user_details or not user_details.get('email') or not user_details.get('username'):
                # returns 401 if any email or / and password is missing
                return make_response(
                    'Could not verify',
                    401,
                    {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
                )
            if True: #check_password_hash(user.password, auth.get('password')):
                # generates the JWT Token
                email=user_details["email"]
                password=user_details["password"]
                username=user_details["username"]
                # date_joined=user_details.get("date_joined")
                user_account = User(email, password, username)
                db.session.add(user_account)
                db.session.commit()
                import os
                # create main folder
                directory=self.app.config['SCRIPT_BASE_PATH']+"\\"+username
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # create output folder in main folder
                directory=self.app.config['SCRIPT_BASE_PATH']+"\\"+username+"\\output"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                return make_response("User Added Successfully", 201)
            # returns 403 if password is wrong
            return make_response(
                'Could not verify',
                403,
                {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
            )
