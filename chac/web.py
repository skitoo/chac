# -*- coding: utf-8 -*-


from flask import Flask, render_template
from .db import Database
from . import settings


app = Flask(__name__)
app.config.from_object(settings)

db = Database(settings.DATABASE_PATH)


@app.route('/')
def index():
    db.graph()
    return render_template('index.html')
