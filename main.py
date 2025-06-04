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
        print("🔍 요청 데이터:", data)

        birthdate = data["birthdate"]
        birthtime = data["birthtime"]
        gender = data["gender"]

        result = get_saju(birthdate, birthtime, gender)
        print("✅ 결과:", result)

        return jsonify(result)
    except Exception as e:
        print("❌ 예외 발생:", e)
        return jsonify({"error": str(e)}), 500

app = app
