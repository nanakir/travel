from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_fanstatic import Fanstatic, init_needed

flights = Flask(__name__)
db = SQLAlchemy(flights)
CsrfProtect(flights)
flights.config.from_object('config')
fanstatic = Fanstatic(flights)
needed = init_needed(base_url='http://0.0.0.0:80')
#flights.config.update(dict(
#    JSON_AS_ASCII = False
#    )
#)

from flights import views, models
