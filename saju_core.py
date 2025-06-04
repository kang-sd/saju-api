from datetime import datetime, timedelta
import sxtwl

tg = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
dz = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 천을귀인 기준 시지 보정: 3.5칸 = 7시간 = 420분 앞당김
def get_hour_branch(hour, minute):
    total_minutes = hour * 60 + minute

    # 지지 배열과 각 지지의 기준 시작 시각(보정 적용)
    shifted_minutes = [
        (dz[i], ((1380 + i * 120 - 420) % 1440)) for i in range(12)
    ]

    # 자시 보정 (자정 이전 시각 대응)
    if total_minutes < shifted_minutes[0][1]:
        total_minutes += 1440

    for i in range(12):
        cur_gz, cur_min = shifted_minutes[i]
        next_min = shifted_minutes[(i + 1) % 12][1] + (1440 if (i + 1) == 0 else 0)
        if cur_min <= total_minutes < next_min:
            return cur_gz

def get_hour_gz(day_tg_index, hour, minute):
    branch = get_hour_branch(hour, minute)
    dz_index = dz.index(branch)
    tg_index = (day_tg_index * 2 + dz_index) % 10
    return tg[tg_index] + branch

def get_luck_direction(gender, day_tg_index):
    is_yang = day_tg_index % 2 == 0
    if gender == "남자":
        return "순행" if is_yang else "역행"
    else:
        return "역행" if is_yang else "순행"

def get_saju(birthdate, birthtime, gender):
    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")

    # 절기 기준 보정 (서울 → 중국)
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
