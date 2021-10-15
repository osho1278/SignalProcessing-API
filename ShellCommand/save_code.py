from flask import Flask, request,redirect,jsonify, url_for,make_response
from Auth import Authenticator
import subprocess
import pickle
import json
import numpy as np
from Models.widgets import WidgetsModel,db
from sqlalchemy import select,insert,update,and_
import os 

class SaveCode:
    def __init__(self,app):
        self.app = app
        self.authenticator = Authenticator()
        self.base_path=self.app.config['SCRIPT_BASE_PATH']
        self.code_suffix=''
        self.code_prefix="""
import numpy as np
from scipy.fftpack import fft
import math
import sys
from math import pi
from scipy import signal
from scipy import integrate
import pandas as pd
import argparse
import pickle
import json
import os

    
args=json.loads(sys.argv[1])
pickleFileName=args["output"]
allParams={}
base_path=r"base_path_fill"
currentStageOutput={}
def save(key,value):
    currentStageOutput[key]=value
    saveOutputToPickle()
def remove(key):
    currentStageOutput.pop(key)
    saveOutputToPickle()
def saveOutputToPickle():    
    with open(os.path.join(base_path,"output",pickleFileName+"_output"), 'wb') as handle:
        pickle.dump(currentStageOutput, handle, protocol=pickle.HIGHEST_PROTOCOL)

if("inherited" in args):
    d=args["inherited"]
    for fileName in d:
        if(fileName):
            with open(os.path.join(base_path,"output",fileName+"_output"), 'rb') as handle:
                prev = pickle.load(handle)
                allParams={**allParams,**prev}
"""
    def add_route(self):
        @self.app.route('/saveCode', methods=['POST'])
        @self.authenticator.token_required
        def saveCode(current_user):
            inp = request.json
            print(inp,current_user)
            id,name=int(current_user['id']),current_user['name']
            output=''
            try:
                code,fileName = inp["code"],inp["fileName"]
                # self.updateArgsinJSON(inp["cmdName"],args)
                statusCode=200
                # cmd = "python ./Scripts/"+inp["cmdName"] + " " + inp["args"]
                # print(cmd)
                f = open(os.path.join(self.base_path,name,fileName+".py"), "w")
                # replace base path
                self.code_prefix = self.code_prefix.replace('base_path_fill',os.path.join(self.base_path,name))
                f.write(self.code_prefix+code+self.code_suffix)
                f.close()
                found={}
                query=select([WidgetsModel]).where(db.and_(WidgetsModel.label==fileName,WidgetsModel.createdBy==id))
                result=db.session.execute(query)
                for res in result:
                    found=res.WidgetsModel.serialized

                obj={}
                obj["label"]=fileName
                obj["data"]={"code":"","parameters":{}}
                if("args" in inp):
                    obj["data"]["parameters"]=inp["args"]
                    
                print(obj)
                if(not found):
                    print("Since custom code "+fileName+" was not found hence ADDING")
                    widgets = WidgetsModel("Code",fileName , obj,"Custom",1)
                    db.session.add(widgets)
                    db.session.commit()
                    # data["Custom"].append(obj)
                else:
                    print("Since custom code "+fileName+"  was found hence Updating")
                    # data["Custom"][id]=obj
                    print(found)
                    found['data']=obj
                    query=update(WidgetsModel).where(db.and_(WidgetsModel.label==fileName,WidgetsModel.createdBy==id)).values(data=obj)
                    db.session.execute(query)
                output='File saved successfully'
            except Exception as e:
                output+=str(e)
                statusCode=500
            print(output)
            return jsonify({'output' : output}), statusCode