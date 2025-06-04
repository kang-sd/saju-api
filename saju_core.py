from datetime import datetime, timedelta
import sxtwl

tg = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
dz = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 시지 보정: 3칸 = 6시간 = 360분 앞당김
def get_hour_branch(hour, minute):
    total_minutes = hour * 60 + minute
    shifted_minutes = [(dz[i], ((1380 + i * 120 - 360) % 1440)) for i in range(12)]

    if total_minutes < shifted_minutes[0][1]:
        total_minutes += 1440

    for i in range(12):
        cur_gz, cur_min = shifted_minutes[i]
        next_min = shifted_minutes[(i + 1) % 12][1] + (1440 if (i + 1) == 0 else 0)
        if cur_min <= total_minutes < next_min:
            return cur_gz

    return shifted_minutes[-1][0]

# 시지의 천간+지지 계산: 공식 기반 (정석)
def get_hour_gz(day_tg_index, hour, minute):
    branch = get_hour_branch(hour, minute)
    dz_index = dz.index(branch)
    tg_index = (day_tg_index * 2 + dz_index) % 10
    return tg[tg_index] + branch

# 대운 방향: 일간 천간 음양 + 성별 기준
def get_luck_direction(gender, day_tg_index):
    is_yang = day_tg_index % 2 == 0
    if gender == "남자":
        return "순행" if is_yang else "역행"
    else:
        return "역행" if is_yang else "순행"

# 전체 사주 계산
def get_saju(birthdate, birthtime, gender):
    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")
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
