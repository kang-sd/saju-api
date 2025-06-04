from datetime import datetime, timedelta
import sxtwl

# 간지 배열
tg = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
dz = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 30분 보정 시지 판단
def get_hour_branch(hour, minute):
    time_in_min = hour * 60 + minute
    if 1350 <= time_in_min or time_in_min < 30:
        return "자"
    elif 30 <= time_in_min < 150:
        return "축"
    elif 150 <= time_in_min < 270:
        return "인"
    elif 270 <= time_in_min < 390:
        return "묘"
    elif 390 <= time_in_min < 510:
        return "진"
    elif 510 <= time_in_min < 630:
        return "사"
    elif 630 <= time_in_min < 750:
        return "오"
    elif 750 <= time_in_min < 870:
        return "미"
    elif 870 <= time_in_min < 990:
        return "신"
    elif 990 <= time_in_min < 1110:
        return "유"
    elif 1110 <= time_in_min < 1230:
        return "술"
    elif 1230 <= time_in_min < 1350:
        return "해"

# 시간지 계산 (전통 보정 + 일간 기반 천간)
def get_hour_gz_fixed(day_tg_index, hour, minute):
    branch = get_hour_branch(hour, minute)
    dz_index = dz.index(branch)
    tg_index = (day_tg_index * 2 + dz_index) % 10
    return tg[tg_index] + branch

# 순행/역행 판단
def get_luck_direction(gender, is_yang_calendar):
    if gender == "남자":
        return "순행" if is_yang_calendar else "역행"
    else:
        return "역행" if is_yang_calendar else "순행"

# 전체 사주 계산
def get_saju(birthdate, birthtime, gender):
    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")
    
    # 중국 기준 보정 (UTC+8 기준 → UTC+9 → -1시간)
    china_dt = dt - timedelta(hours=1)
    lunar = sxtwl.fromSolar(china_dt.year, china_dt.month, china_dt.day)

    year_gz = tg[lunar.getYearGZ().tg] + dz[lunar.getYearGZ().dz]
    month_gz = tg[lunar.getMonthGZ().tg] + dz[lunar.getMonthGZ().dz]
    day_gz = tg[lunar.getDayGZ().tg] + dz[lunar.getDayGZ().dz]
    hour_gz = get_hour_gz_fixed(lunar.getDayGZ().tg, dt.hour, dt.minute)

    is_yang = lunar.getLunarYear() % 2 == 0
    luck_dir = get_luck_direction(gender, is_yang)

    return {
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
        "hour": hour_gz,
        "gender": gender,
        "luck_direction": luck_dir
    }
