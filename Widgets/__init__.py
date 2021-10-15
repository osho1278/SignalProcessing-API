from flask import Flask, request, redirect, jsonify, url_for, make_response
from Auth import Authenticator
import subprocess
import json
from Models.widgets import WidgetsModel,db
from sqlalchemy import select,delete,or_

class Widgets:
    def __init__(self, app):
        self.app = app
        self.authenticator = Authenticator()

    def add_route(self):
        @self.app.route('/widgets', methods=['GET'])
        @self.authenticator.token_required
        def widgets(current_user):
            data={}
            id,name=int(current_user['id']),current_user['name']
            statusCode=200
            try:
                query=select([WidgetsModel]).where(db.or_(WidgetsModel.function_type=="PreBuiltFunctions",WidgetsModel.createdBy==id))
                result=db.session.execute(query)
                for res in result:
                    d=res.WidgetsModel.serialized
                    if(d["function_type"] not in data):
                        data[d["function_type"]]=[]
                    data[d["function_type"]].append(d)
                    print(res)
            except Exception as e:
                statusCode=501
            # f = open('C:\\Users\\osbajpai\\iot-platform\\iot\\Scripts\\widgets.json','r')
            # data = json.load(f)
            return jsonify({'data': data}), statusCode

        @self.authenticator.token_required
        @self.app.route('/widgets', methods=['POST'])
        def addWidgets():
            data = request.json
            print(data)
            message="Added Successfully"
            statusCode=200
            try:
                widgets = WidgetsModel(data["category"], data["label"], data["data"],data["function_type"],data["createdBy"])
                db.session.add(widgets)
                db.session.commit()
            except Exception as e:
                print(e)
                message='Unable to add'
                statusCode=500

            return jsonify({'data': message}), statusCode