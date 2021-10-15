from flask import Flask, request,redirect,jsonify, url_for,make_response
from Auth import Authenticator
import subprocess
import pickle
import json
import numpy as np
from .output import Output
from .stats import Stats
from .save_code import SaveCode
from .file_upload import FileUpload
import os

class ShellCommand:
    def __init__(self,app):
        self.app = app
        self.authenticator=Authenticator()
        self.base_path=self.app.config['SCRIPT_BASE_PATH']
        self.python=self.app.config['PYTHON']
        Output(self.app).add_route()
        SaveCode(self.app).add_route()
        FileUpload(self.app).add_route()
        Stats(self.app).add_route()

    def updateArgsinJSON(self,cmd,args):
        f = open(os.path.join(self.base_path,'widgets.json'))
        data = json.load(f)
        done=False
        try:
            for key in data:
                parent=key
                id=0
                for val in data[key]:
                    # print("VAL ===",val)
                    if(val["label"] in cmd):
                        for argkey in args:
                            # if(argkey in data[key][id]["data"]["parameters"] )
                            data[key][id]["data"]["parameters"][argkey] = args[argkey]
                        done=True
                        break
                    id+=1
                if(done):
                    break

            with open(os.path.join(self.base_path,'widgets.json'), 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Got an exception : ",e)
    def add_route(self):
        @self.app.route('/command', methods=['POST'])
        @self.authenticator.token_required
        def shellCommand(current_user):
            inp = request.json
            print(inp)
            output=''
            id,name=int(current_user['id']),current_user['name']
            statusCode=200
            cmd = self.python+" " +os.path.join(self.base_path,name,inp["cmdName"]) + " " + json.dumps(inp["args"])
            print(cmd)
            args=inp["args"]
            print(args)
            # self.updateArgsinJSON(cmd, args)
            try:
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
            print(output)
            return jsonify({'output' : output}), statusCode