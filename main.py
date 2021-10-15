import os
from flask import Flask, redirect, url_for
from Auth.Login import Login
from Auth.Signup import Signup
from Graph import Graph
from ShellCommand import ShellCommand
from  Widgets import Widgets
from flask_cors import CORS, cross_origin
from Models import db
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os 

class Api:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['PYTHON']='python'
        self.app.config['CORS_HEADERS'] = 'Content-Type:application/json'
        self.app.config['SCRIPT_BASE_PATH'] = os.path.join('C:',os.sep,'Users','osbajpai','iot-platform','iot','Scripts')
        # self.app.config['SCRIPT_BASE_PATH'] = os.path.join('home','azureuser','userdata')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Pass2020!@localhost:5432/signalProcessing"
        CORS(self.app,resources={r"/*": {"origins": "*"}})
        db.init_app(self.app)
        engine = create_engine(self.app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
        # Create database if it does not exist.
        if not database_exists(engine.url):
            create_database(engine.url)
        else:
            # Connect the database if exists.
            engine.connect()
        Migrate(self.app, db)
        from Models import user,graph,widgets,output
        with self.app.app_context():
            db.create_all()

        self.auth=Login(self.app)
        self.signup=Signup(self.app)
        self.shell_command=ShellCommand(self.app)
        self.widgets=Widgets(self.app)
        self.graph=Graph(self.app)
    def run(self):
        self.app.run(host='0.0.0.0',debug = True)

    def add_route(self):
        self.auth.add_route()
        self.signup.add_route()
        self.shell_command.add_route()
        self.widgets.add_route()
        self.graph.add_route()


if __name__ == '__main__':
    api=Api()
    api.add_route()
    api.run()