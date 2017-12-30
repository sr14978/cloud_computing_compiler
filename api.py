from flask import Flask, Blueprint, request
from pubsub import pubsub
api = Blueprint('api_blueprint', __name__)

@api.route("/")
def home():
    return "api home"
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    pubsub.add_breakup_job(data='{"type": "breakup", "path": "<path_on_blob>"}')
    return 200

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
