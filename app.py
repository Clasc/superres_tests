from flask import Flask, request
from main import hello_world, superres

app = Flask(__name__)


@app.route("/")
def index():
    return hello_world(request)


@app.route("/superres", methods=["POST"])
def superres_req():
    return superres(request)
