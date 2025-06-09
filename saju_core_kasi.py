import requests
import urllib.parse
from datetime import datetime, timedelta

# 천간 지지 시주 표
TIME_HEAVENLY_STEM_TABLE = {
    '갑': ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계', '갑', '을'],
    '을': ['병', '정', '무', '기', '경', '신', '임', '계', '갑', '을', '병', '정'],
    '병': ['무', '기', '경', '신', '임', '계', '갑', '을', '병', '정', '무', '기'],
    '정': ['경', '신', '임', '계', '갑', '을', '병', '정', '무', '기', '경', '신'],
    '무': ['임', '계', '갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'],
    '기': ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계', '갑', '을'],
    '경': ['병', '정', '무', '기', '경', '신', '임', '계', '갑', '을', '병', '정'],
    '신': ['무', '기', '경', '신', '임', '계', '갑', '을', '병', '정', '무', '기'],
    '임': ['경', '신', '임', '계', '갑', '을', '병', '정', '무', '기', '경', '신'],
    '계': ['임', '계', '갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'],
}

TIME_EARTHLY_BRANCHES = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']

def get_saju_from_kasi_api(year, month, day, service_key):
    base_url = "https://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getLrsrCldInfo"
    params = {
        "solYear": year,
        "solMonth": month,
        "solDay": day,
        "ServiceKey": service_key,
        "_type": "json"
    }
    url = f"{base_url}?{'&'.join(f'{k}={urllib.parse.quote(str(v))}' for k,v in params.items())}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: 상태 코드 {response.status_code}")

    data = response.json()

    result = {
        'lunar_date': '',
        'weekday': '',
        'ganji_year': '',
        'ganji_month': '',
        'ganji_day': ''
    }

    try:
        body = data['response']['body']
        items = body['items']['item']
        item = items[0] if isinstance(items, list) else items
        result['lunar_date'] = item.get('lunDay', '')
        result['weekday'] = item.get('weekday', '')
        result['ganji_year'] = item.get('ganjiYear', '')
        result['ganji_month'] = item.get('ganjiMonth', '')
        result['ganji_day'] = item.get('ganjiDay', '')
    except Exception:
        raise ValueError("API 응답 파싱 실패")

    return result

def calculate_hour_stem_branch(birthtime: str, day_stem: str):
    birth_time = datetime.strptime(birthtime, '%H:%M')
    corrected_time = birth_time - timedelta(minutes=30)
    total_minutes = corrected_time.hour * 60 + corrected_time.minute
    index = (total_minutes // 120) % 12
    hour_branch = TIME_EARTHLY_BRANCHES[index]
    hour_stem = TIME_HEAVENLY_STEM_TABLE[day_stem][index]
    return hour_stem, hour_branch
