from flask import Flask, request, abort
from flask.wrappers import Response
from main import upscale

app = Flask(__name__)


@app.route("/upscale", methods=["POST"])
def post():
    data = request.get_json()
    if data is None or data["image"] is None:
        abort(400, "Image is missing from data")
    result = upscale(data["image"])
    return Response(result)
