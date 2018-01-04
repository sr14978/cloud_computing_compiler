from flask import Flask, redirect, render_template
import database
from oauth2client.contrib.flask_util import UserOAuth2

oauth2 = UserOAuth2()

app = Flask(__name__)

oauth2.init_app(
        app,
        scopes=['email', 'profile'],
        authorize_callback=_request_user_info)

@app.route("/")
def index():
    return redirect('/static/index.html')
    
@app.route("/history/<user_id>")
def history(user_id):
    user = database.get_user(user_id)
    if user != None:
        return render_template('history.html', executables=user['executables'])
    else:
        return "Invalid user", 401

@app.route("/test")
@oauth2.required
def test()
    return "Test oauth2", 200
 
 
def _request_user_info(creds):
    print("credentials: " + str(creds))




