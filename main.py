from flask import Flask, request, jsonify
import saju_core_kasi as saju_core

app = Flask(__name__)

@app.route("/saju", methods=["POST"])
def run():
    data = request.get_json()
    birthdate = data.get('birthdate')
    birthtime = data.get('birthtime', '')
    gender = data.get('gender', '')
    luck_direction = data.get('luck_direction', '')
    service_key = "FwaCOA5XZ5lXe79WuR%2BRMCHT4BJ1M5XWYuRlsvv%2FlkGHAgw5dbATp%2FA6Kek5%2FarQcqD1%2FslrxehpzYcsGaNhTw%3D%3D"
url = f"http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getSolCalInfo?ServiceKey={service_key}&solYear={year}&solMonth={str(month).zfill(2)}&solDay={str(day).zfill(2)}&_type=json"

    year, month, day = map(int, birthdate.split('-'))
    result = saju_core.get_saju_from_kasi_api(year, month, day, service_key)
    hour_gan, hour_branch = saju_core.calculate_hour_stem_branch(birthtime, result['ganji_day'][0])
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
