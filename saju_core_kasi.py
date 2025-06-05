import requests

# 시지 시간표 (이미 보정된 시간 기준)
TIME_BRANCH_TABLE = [
    ("23:30", "01:29", "자"),
    ("01:30", "03:29", "축"),
    ("03:30", "05:29", "인"),
    ("05:30", "07:29", "묘"),
    ("07:30", "09:29", "진"),
    ("09:30", "11:29", "사"),
    ("11:30", "13:29", "오"),
    ("13:30", "15:29", "미"),
    ("15:30", "17:29", "신"),
    ("17:30", "19:29", "유"),
    ("19:30", "21:29", "술"),
    ("21:30", "23:29", "해"),
]

# 천간 시주표 (네가 준 최신 표)
HOUR_STEM_TABLE = {
    "갑": ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계", "갑", "을"],
    "을": ["병", "정", "무", "기", "경", "신", "임", "계", "갑", "을", "병", "정"],
    "병": ["무", "기", "경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"],
    "정": ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기", "경", "신"],
    "무": ["임", "계", "갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"],
    "기": ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계", "갑", "을"],
    "경": ["병", "정", "무", "기", "경", "신", "임", "계", "갑", "을", "병", "정"],
    "신": ["무", "기", "경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"],
    "임": ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기", "경", "신"],
    "계": ["임", "계", "갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"],
}

def get_saju_from_kasi_api(year: int, month: int, day: int, service_key: str):
    url = f"http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getSolCalInfo?ServiceKey={service_key}&solYear={year}&solMonth={str(month).zfill(2)}&solDay={str(day).zfill(2)}&_type=json"
    res = requests.get(url)
    print(f"API 요청 URL: {url}")
    print(f"응답 상태 코드: {res.status_code}")
    print(f"응답 내용(최대 500자): {res.text[:500]}")
    if res.status_code != 200:
        raise Exception(f"API 요청 실패: 상태코드 {res.status_code}")
    try:
        data = res.json()["response"]["body"]["items"]["item"]
    except Exception as e:
        raise Exception(f"API 응답 JSON 파싱 실패: {e}")

    return {
        "lunar_date": f"{data['lunYear']}-{data['lunMonth'].zfill(2)}-{data['lunDay'].zfill(2)}",
        "weekday": data["weekday"],
        "ganji_year": data["sYear"],
        "ganji_month": data["sMonth"],
        "ganji_day": data["sDay"],
    }

def calculate_hour_stem_branch(birthtime: str, day_stem: str):
    hour = int(birthtime.split(":")[0])
    minute = int(birthtime.split(":")[1])
    total_min = hour * 60 + minute

    for i, (start, end, branch) in enumerate(TIME_BRANCH_TABLE):
        sh, sm = map(int, start.split(":"))
        eh, em = map(int, end.split(":"))
        start_min = sh * 60 + sm
        end_min = eh * 60 + em

        if start_min <= end_min:
            if start_min <= total_min <= end_min:
                time_branch = branch
                break
        else:
            if total_min >= start_min or total_min <= end_min:
                time_branch = branch
                break
    else:
        raise Exception("해당 시간에 맞는 시지 없음")

    branch_index = ["자","축","인","묘","진","사","오","미","신","유","술","해"].index(time_branch)
    time_stem = HOUR_STEM_TABLE[day_stem][branch_index]
    return time_stem, time_branch
