from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

# status_db = SQLAlchemy(app)
# store_info_db = SQLAlchemy(app)
db = SQLAlchemy(app)

from src import routes