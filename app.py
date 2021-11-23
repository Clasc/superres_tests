from flask import Flask, request
from superres import supperresVideo

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/superres")
def superres():
    input = request.args.get("in")
    out = request.args.get("out")
    print(input, out)
    if input is None or out is None:
        return "error, missing arguments"
    supperresVideo(input, out)
    return "Done!"
