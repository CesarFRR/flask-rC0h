from flask import Flask, render_template, request, redirect, url_for
import os
import database as db


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=5000)
