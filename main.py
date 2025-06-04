from flask import Flask, request, jsonify
from saju_core import get_saju

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/saju', methods=['POST'])
def saju():
    try:
        data = request.json
        birthdate = data["birthdate"]
        birthtime = data["birthtime"]
        gender = data["gender"]
        result = get_saju(birthdate, birthtime, gender)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

app = app