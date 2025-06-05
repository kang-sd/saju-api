from flask import Flask, request, jsonify
import saju_core_kasi as saju_core

app = Flask(__name__)

SERVICE_KEY = "jyD7ufDh6n1ZbE%2BzzZ2mgo%2F5Ef1%2B8r2xEdGqFAkULVnMUMjfkT%2FzMQZIhB8x5mSDp3jK0xaw7ZxQlz0p%2BHLgDg%3D%3D"

@app.route("/saju", methods=["POST"])
def run():
    data = request.get_json()
    birthdate = data.get('birthdate')
    birthtime = data.get('birthtime', '')
    gender = data.get('gender', '')
    luck_direction = data.get('luck_direction', '')

    if not birthdate:
        return jsonify({'error': 'birthdate is required'}), 400

    try:
        year, month, day = map(int, birthdate.split('-'))
    except Exception:
        return jsonify({'error': 'Invalid birthdate format'}), 400

    try:
        result = saju_core.get_saju_from_kasi_api(year, month, day, SERVICE_KEY)
    except Exception as e:
        return jsonify({'error': f'API 호출 실패: {str(e)}'}), 500

    day_stem = result['ganji_day'][0]
    hour_gan, hour_branch = saju_core.calculate_hour_stem_branch(birthtime, day_stem)
    result['ganji_hour'] = f"{hour_gan}{hour_branch}"

    return jsonify({
        'birthdate': birthdate,
        'lunar_date': result['lunar_date'],
        'weekday': result['weekday'],
        'ganji': {
            'year': result['ganji_year'],
            'month': result['ganji_month'],
            'day': result['ganji_day'],
            'hour': result['ganji_hour']
        },
        'birthtime': birthtime,
        'gender': gender,
        'luck_direction': luck_direction
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
