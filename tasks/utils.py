from os import stat
import audioread
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

def validate_password(password):
    val = True
    if not any(char.isdigit() for char in password):
        val = False
    if not any(c.isalpha() for c in password):
        val = False
    if val:
        return val


def duration(file):
    try:
        with audioread.audio_open(file) as f:
            totalsec = f.duration
            min, sec = divmod(totalsec, 60)
            return "{:02d}:{:02d}".format(int(min), int(sec))
    except:
        return "00:00"

def is_date_valid(imputdate):
    date_years = relativedelta(date.today(), datetime.strptime(imputdate, "%Y-%m-%d")).years
    if date_years >= 18 :
        return True
    else:
        return False


def is_date_future_date(inputdate):
    date_format = "%Y-%m-%d"
    end = datetime.strptime(inputdate, date_format)
    now = datetime.strptime(str(datetime.date(datetime.now())), date_format)
    if end < now:
        return False
    else:
        return True