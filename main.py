from flask import Flask, request, jsonify
import saju_core_kasi as saju_core

app = Flask(__name__)

@app.route("/saju", methods=["POST"])
def run():
    try:
        data = request.get_json()
        birthdate = data.get('birthdate')
        birthtime = data.get('birthtime', '')
        gender = data.get('gender', '')
        luck_direction = data.get('luck_direction', '')
        service_key = "jyD7ufDh6n1ZbE%2BzzZ2mgo%2F5Ef1%2B8r2xEdGqFAkULVnMUMjfkT%2FzMQZIhB8x5mSDp3jK0xaw7ZxQlz0p%2BHLgDg%3D%3D"

        year, month, day = map(int, birthdate.split('-'))
        result = saju_core.get_saju_from_kasi_api(year, month, day, service_key)
        hour_gan, hour_branch = saju_core.calculate_hour_stem_branch(birthtime, result['ganji_day'])
        result['ganji_hour'] = f"{hour_gan}{hour_branch}"

        return jsonify({
            'birthdate': birthdate,
            'lunar_date': result.get('lunar_date', ''),
            'weekday': result.get('weekday', ''),
            'ganji': {
                'year': result.get('ganji_year', ''),
                'month': result.get('ganji_month', ''),
                'day': result.get('ganji_day', ''),
                'hour': result.get('ganji_hour', '')
            },
            'birthtime': birthtime,
            'gender': gender,
            'luck_direction': luck_direction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
