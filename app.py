from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib



client = MongoClient()
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signup.html')


@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)

@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    # Let's also handle the case where the id and
    # password combination cannot be found
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)