from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import BaseConfig
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from .models import *



