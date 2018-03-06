
import os
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, jsonify
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return str(self.id)


@app.route('/')
@login_required
def home():
    return Response("You are viewing protected content.")

@app.route("/login")
def login():
    login_user(User(0))
    return jsonify({'message': 'Logged in to Flask.'})

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out of Flask.'})

@app.route("/demo")
def show_demo():
    return render_template('demo.html')

@app.errorhandler(401)
def access_denied(e):
    return jsonify({'error_description': 'You need to log in to retrieve this data.'})

@login_manager.user_loader
def load_user(userid):
    return User(userid)
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)