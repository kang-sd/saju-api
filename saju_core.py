from datetime import datetime
import sxtwl

tg = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
dz = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
yy = ['양', '음']

def get_hour_gz(day_tg_index, hour):
    dz_index = ((hour + 1) // 2) % 12
    tg_index = (day_tg_index * 2 + dz_index) % 10
    return tg[tg_index] + dz[dz_index]

def get_luck_direction(gender, is_yang_calendar):
    if gender == "남자":
        return "순행" if is_yang_calendar else "역행"
    else:
        return "역행" if is_yang_calendar else "순행"

def get_saju(birthdate, birthtime, gender):
    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")
    lunar = sxtwl.fromSolar(dt.year, dt.month, dt.day)

    year_gz = tg[lunar.getYearGZ().tg] + dz[lunar.getYearGZ().dz]
    month_gz = tg[lunar.getMonthGZ().tg] + dz[lunar.getMonthGZ().dz]
    day_gz = tg[lunar.getDayGZ().tg] + dz[lunar.getDayGZ().dz]
    hour_gz = get_hour_gz(lunar.getDayGZ().tg, dt.hour)

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