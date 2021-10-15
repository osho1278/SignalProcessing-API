from flask import Flask,request, jsonify,redirect, url_for
from Auth import Authenticator
import json
import pickle
from Models import db
from Models.graph import GraphModel
from Models.user import User
from sqlalchemy.sql import select,delete

class Graph:
    def __init__(self,app):
        self.app = app
        self.authenticator=Authenticator()
        self.base_path = self.app.config['SCRIPT_BASE_PATH']

    def add_route(self):
        @self.app.route('/graph', methods=['POST'])
        @self.authenticator.token_required
        def saveGraph(current_user):
            inp = request.json
            print(inp)
            data=''
            statusCode=200
            try:
                graph_data = GraphModel( inp["graphName"],inp["graph"], current_user["id"])
                db.session.add(graph_data)
                db.session.commit()
            except Exception as e:
                statusCode=501
                print(e)
            return jsonify({'output' : data}), statusCode

        @self.app.route('/graph', methods=['GET'])
        @self.authenticator.token_required
        def getGraph(current_user):
            print("Getting Graph")
            data=[]
            
            statusCode=200
            try:
                query = select([User,GraphModel]).where(GraphModel.createdBy==current_user["id"],User.id==current_user["id"])
                results=db.session.execute(query)
                for row in results:
                    data.append({**row.User.serialized,**row.GraphModel.serialized})
            except Exception as e:
                statusCode=501
                print(e)
            return jsonify({'output' : data}), statusCode
        
        # @self.app.route('/graphById', methods=['GET'])
        # @self.authenticator.token_required
        # def getGraphById(current_user):
        #     print("Getting Graph")
        #     data=[]
        #     statusCode=200
        #     try:
        #         with open(self.base_path+'\\graph.pkl', 'rb') as handle:
        #             data=pickle.load(handle,encoding="utf8")
        #             print(data)
        #     except Exception as e:
        #         statusCode=501
        #         print(e)
        #     return jsonify({'output' : data}), statusCode
        
        @self.app.route('/deleteGraph', methods=['POST'])
        @self.authenticator.token_required
        def deleteGraph(current_user):
            data = request.json
            print(data)
            message="Deleted Successfully"
            statusCode=200
            try:
                query=delete(GraphModel).where(GraphModel.id==data['id'])
                print(query)
                result=db.session.execute(query)
                db.session.commit()
            except Exception as e:
                print(e)
                message='Unable to Delete'
                statusCode=500

            # f = open('C:\\Users\\osbajpai\\iot-platform\\iot\\Scripts\\widgets.json','r')
            # data = json.load(f)
            return jsonify({'data': message}), statusCode
