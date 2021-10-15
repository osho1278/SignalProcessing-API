from flask import Flask, request,redirect,jsonify, url_for,make_response
from Auth import Authenticator
import subprocess
import pickle
import json
import numpy as np
from Models.widgets import WidgetsModel,db
from sqlalchemy import select,insert,update,and_
import os

class FileUpload:
    def __init__(self,app):
        self.app = app
        self.authenticator = Authenticator()
        self.python=self.app.config['PYTHON']

        self.base_path=self.app.config['SCRIPT_BASE_PATH']
        self.code_suffix=''
        self.code_prefix="""

"""
    def add_route(self):
        @self.app.route('/fileUpload', methods=['POST'])
        @self.authenticator.token_required
        def fileUpload(current_user):
            message="File Uploaded"
            id,name=int(current_user['id']),current_user['name']
            statusCode=200
            output=''
            try:
                f = request.files['file']
                f.save(self.base_path+"/CSV")
                cmd = self.python+" " +os.path.join(self.base_path,name,"dataframe.py")+" -f "+os.path.join(self.base_path,"CSV") + " -o "+os.path.join(self.base_path,"output","CSV_output")
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if(p.stdout):
                    for line in p.stdout.readlines():
                        print(line)
                        output+=line.decode("utf-8") 
                elif(p.stderr):
                    for line in p.stderr.readlines():
                        statusCode=500
                        output+=line.decode("utf-8") 
                else:
                    raise Exception('Invalid command ')
   
                # print("Retval",retval)
            except Exception as e:
                output+=e.decode("utf-8") 
                statusCode=500
                message ="Unable to upload file"            
            print(output)
            return jsonify({'output' : message}), statusCode
            