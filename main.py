#!/usr/bin/python

from bottle import Bottle, run
import entities

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

run(app, host='localhost', port=8080)
