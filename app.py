from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient()
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/article')
def article():
    return render_template('article.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)