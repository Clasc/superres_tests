from flask import Flask, request
from main import superres

app = Flask(__name__)

@app.route("/superres", methods=["POST"])
def post():
    print("received POST request")
    message = superres(request)
    return message
