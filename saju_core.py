from datetime import datetime, timedelta
import sxtwl

# 천간 / 지지
tg = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
dz = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 천을귀인 기준으로 시지 구간 3지지 앞당겨 설정
def get_hour_branch(hour, minute):
    total_minutes = hour * 60 + minute

    # 기준 구간 (시작 시각 기준)
    original = [
        ("자", 1380),   # 23:00
        ("축", 60),     # 01:00
        ("인", 180),
        ("묘", 300),
        ("진", 420),
        ("사", 540),
        ("오", 660),
        ("미", 780),
        ("신", 900),
        ("유", 1020),
        ("술", 1140),
        ("해", 1260)
    ]

    # 지지 3칸 앞당김
    shifted = [(dz[(dz.index(gz) + 3) % 12], start) for gz, start in original]

    if total_minutes < 60:
        total_minutes += 1440  # 자시 보정

    for i in range(12):
        cur_gz, cur_min = shifted[i]
        next_min = shifted[(i + 1) % 12][1] + (1440 if (i + 1) == 0 else 0)
        if cur_min <= total_minutes < next_min:
            return cur_gz

# 시지 천간지지 조합
def get_hour_gz(day_tg_index, hour, minute):
    branch = get_hour_branch(hour, minute)
    dz_index = dz.index(branch)
    tg_index = (day_tg_index * 2 + dz_index) % 10
    return tg[tg_index] + branch

# 대운 방향 계산
def get_luck_direction(gender, day_tg_index):
    is_yang = day_tg_index % 2 == 0
    if gender == "남자":
        return "순행" if is_yang else "역행"
    else:
        return "역행" if is_yang else "순행"

# 메인 사주 계산
def get_saju(birthdate, birthtime, gender):
    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")

    # 중국 절기 기준: 서울 기준 -1시간 보정
    china_dt = dt - timedelta(hours=1)
    lunar = sxtwl.fromSolar(china_dt.year, china_dt.month, china_dt.day)

    year_gz = tg[lunar.getYearGZ().tg] + dz[lunar.getYearGZ().dz]
    month_gz = tg[lunar.getMonthGZ().tg] + dz[lunar.getMonthGZ().dz]
    day_gz_index = lunar.getDayGZ().tg
    day_gz = tg[day_gz_index] + dz[lunar.getDayGZ().dz]
    hour_gz = get_hour_gz(day_gz_index, dt.hour, dt.minute)
    luck_dir = get_luck_direction(gender, day_gz_index)

    return {
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
        "hour": hour_gz,
        "gender": gender,
        "luck_direction": luck_dir
    }
