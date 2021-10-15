from flask import Flask, request,redirect,jsonify, url_for,make_response
from Auth import Authenticator
import subprocess
import pickle
import json
import numpy as np
import os 

class Output:
    def __init__(self,app):
        self.app = app
        self.authenticator = Authenticator()
        self.base_path=self.app.config['SCRIPT_BASE_PATH']
        self.python=self.app.config['PYTHON']

    def add_route(self):
        @self.app.route('/commandOutput')
        @self.authenticator.token_required
        def commandOutput(current_user):
            fileName = request.args.get('fileName')
            id,name=int(current_user['id']),current_user['name']
            statusCode=200
            output=None
            with open(os.path.join(self.base_path,name,"output",fileName+"_output"), 'rb') as handle:
                output = str(pickle.load(handle))
                output.replace("n", "???")
            if(not output):
                statusCode=500
            return jsonify({'output' : output}), statusCode
        
        @self.app.route('/commandOutputParams')
        @self.authenticator.token_required
        def commandOutputParams(current_user):
            fileNames = request.args.get('fileName').split(",")
            id,name=int(current_user['id']),current_user['name']
            statusCode=200
            output={}
            for fileName in fileNames:
                if(fileName):
                    with open(os.path.join(self.base_path,name,"output",fileName+"_output"), 'rb') as handle:
                        keys=list(pickle.load(handle).keys())
                        output[fileName]=keys
                    # output.replace("n", "???")
            if(not output):
                statusCode=500
            return jsonify({'output' : output}), statusCode