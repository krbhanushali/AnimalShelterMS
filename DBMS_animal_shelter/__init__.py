"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

local_server = True

app = Flask(__name__)

app.secret_key = 'pswd123'

app.config['SQLALCHEMY_DATABASE_URI']=  'mysql://root:pswd@localhost/AnimalShelterMS'


import DBMS_animal_shelter.views
