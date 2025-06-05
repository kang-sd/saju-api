import requests
import xml.etree.ElementTree as ET

def get_saju_from_kasi_api(year, month, day, service_key):
    url = (
        "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getLunCalInfo"
        f"?solYear={year}&solMonth={month:02d}&solDay={day:02d}&ServiceKey={service_key}"
    )
    response = requests.get(url)
    root = ET.fromstring(response.content)
    item = root.find('.//item')
    if item is None:
        raise ValueError("API 응답 오류 또는 항목 없음")
    return {
        'ganji_year': item.findtext('lunSecha'),
        'ganji_month': item.findtext('lunWolgeon'),
        'ganji_day': item.findtext('lunIljin'),
        'weekday': item.findtext('solWeek'),
        'lunar_date': f"{item.findtext('lunYear')}-{item.findtext('lunMonth')}-{item.findtext('lunDay')}",
        'leap_month': item.findtext('lunLeapmonth')
    }

def calculate_hour_stem_branch(birthtime, day_gan):
    hour_map = [
        (23, 1, '자'), (1, 3, '축'), (3, 5, '인'), (5, 7, '묘'),
        (7, 9, '진'), (9, 11, '사'), (11, 13, '오'), (13, 15, '미'),
        (15, 17, '신'), (17, 21, '유'), (21, 23, '술'), (23, 24, '해')
    ]
    zi_gan_map = {
        '갑': ['갑','을','병','정','무','기','경','신','임','계','갑','을'],
        '을': ['병','정','무','기','경','신','임','계','갑','을','병','정'],
        '병': ['무','기','경','신','임','계','갑','을','병','정','무','기'],
        '정': ['경','신','임','계','갑','을','병','정','무','기','경','신'],
        '무': ['임','계','갑','을','병','정','무','기','경','신','임','계'],
        '기': ['병','정','무','기','경','신','임','계','갑','을','병','정'],
        '경': ['병','정','무','기','경','신','임','계','갑','을','병','정'],
        '신': ['무','기','경','신','임','계','갑','을','병','정','무','기'],
        '임': ['경','신','임','계','갑','을','병','정','무','기','경','신'],
        '계': ['임','계','갑','을','병','정','무','기','경','신','임','계'],
    }
    try:
        hour, minute = map(int, birthtime.strip().split(":"))
        minute -= 30
        if minute < 0:
            minute += 60
            hour -= 1
        if hour < 0:
            hour = 23
        hour_branch = None
        for start, end, branch in hour_map:
            if start <= hour < end or (start == 23 and hour == 0):
                hour_branch = branch
                break
        if hour_branch is None:
            return "시간오류", "시간오류"
        day_gan_clean = day_gan[0]
        if day_gan_clean not in zi_gan_map:
            return "일간오류", hour_branch
        idx = ['자','축','인','묘','진','사','오','미','신','유','술','해'].index(hour_branch)
        hour_gan = zi_gan_map[day_gan_clean][idx]
        return hour_gan, hour_branch
    except:
        return "시간오류", "시간오류"
