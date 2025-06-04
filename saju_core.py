from datetime import datetime, timedelta
import sxtwl

# 천간 / 지지
tg = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
dz = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 시지 30분 보정
def get_hour_branch(hour, minute):
    total_minutes = hour * 60 + minute
    if total_minutes >= 1350 or total_minutes < 30:
        return "자"
    elif 30 <= total_minutes < 150:
        return "축"
    elif 150 <= total_minutes < 270:
        return "인"
    elif 270 <= total_minutes < 390:
        return "묘"
    elif 390 <= total_minutes < 510:
        return "진"
    elif 510 <= total_minutes < 630:
        return "사"
    elif 630 <= total_minutes < 750:
        return "오"
    elif 750 <= total_minutes < 870:
        return "미"
    elif 870 <= total_minutes < 990:
        return "신"
    elif 990 <= total_minutes < 1110:
        return "유"
    elif 1110 <= total_minutes < 1230:
        return "술"
    elif 1230 <= total_minutes < 1350:
        return "해"

# 시지의 천간+지지 구하기
def get_hour_gz(day_tg_index, hour, minute):
    branch = get_hour_branch(hour, minute)
    dz_index = dz.index(branch)
    tg_index = (day_tg_index * 2 + dz_index) % 10
    return tg[tg_index] + branch

# 대운방향: 일간 음양 기준
def get_luck_direction(gender, day_tg_index):
    is_yang = day_tg_index % 2 == 0
    if gender == "남자":
        return "순행" if is_yang else "역행"
    else:
        return "역행" if is_yang else "순행"

# 사주 계산
def get_saju(birthdate, birthtime, gender):
    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")

    # 서울(KST) → 중국(CST) 기준으로 -1시간 보정
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
