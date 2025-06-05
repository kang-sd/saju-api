import requests
import urllib.parse

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

    # 실제 API JSON 구조에 맞게 값 추출 코드 작성 필요
    # 예시는 임시로 빈 값 할당
    result = {
        'lunar_date': '',  
        'weekday': '',
        'ganji_year': '',
        'ganji_month': '',
        'ganji_day': ''
    }

    # data 에서 실제 값 파싱 예
    try:
        body = data['response']['body']
        items = body['items']['item']
        # items가 리스트인지 단일 dict인지 체크 후 처리
        if isinstance(items, list):
            item = items[0]
        else:
            item = items
        result['lunar_date'] = item.get('lunDay', '')
        result['weekday'] = item.get('weekday', '')
        result['ganji_year'] = item.get('lunYear', '')
        result['ganji_month'] = item.get('lunMonth', '')
        result['ganji_day'] = item.get('lunDay', '')
    except Exception:
        pass

    return result

def calculate_hour_stem_branch(birthtime, ganji_day):
    # 표준화된 표로 시간 천간/지지 계산 로직 작성
    # 예시 임시 반환
    hour_gan = '갑'
    hour_branch = '자'
    return hour_gan, hour_branch
