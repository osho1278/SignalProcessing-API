from flask import Flask, request,redirect,jsonify, url_for,make_response
from Auth import Authenticator
import subprocess
import pickle
import json
import numpy as np
import os 

class Stats:
    def __init__(self,app):
        self.app = app
        self.authenticator = Authenticator()
        self.base_path=self.app.config['SCRIPT_BASE_PATH']
    def add_route(self):    
        @self.app.route('/visualizeData')
        @self.authenticator.token_required
        def visualizeData(current_user):
            fileNames = request.args.get('stage').split(",")
            id,name=int(current_user['id']),current_user['name']
            print(fileNames)
            statusCode=200
            limit=1000
            output=[{} for i in range(limit)]
            temp={}
            keys=[]
            try:
                for fileName in  fileNames:
                    with open(os.path.join(self.base_path,name,"output",fileName+"_output"), 'rb') as handle:
                        temp = pickle.load(handle)
                        print(temp)
                        print(type(temp))
                        print(temp)
                        # output.append({"keys":list(temp.keys())})
                        for key in temp:
                            keyName = fileName+"."+key
                            keys.append(keyName)
                            val=temp[key]
                            print(type(val))
                            if('ndarray' in str(type(val)) or 'list' in str(type(val)) ):
                                li=np.array(val).tolist()
                                ct=0
                                for value in li[:limit]:
                                    output[ct][keyName] = value  #,"index":ct})
                                    ct+=1
                            else:
                                output.append({keyName:val})
                        if(not output):
                            statusCode=500
            except Exception as e:
                print("Exception  :",e)
            return jsonify({'output' : output,"keys":keys}), statusCode