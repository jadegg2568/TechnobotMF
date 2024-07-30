from datetime import datetime
import pytz
import os


def get_date():
    return datetime.now(pytz.timezone("Europe/Moscow")).strftime("%D").replace("/", ".")


def get_time():
    return datetime.now(pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S")


def create_file():
    _path = f"records/{get_date()}.log"
    num = 2
    while os.path.exists(_path):
        _path = f"records/{get_date()}_{num}.log"
        num += 1
    open(_path, "w", encoding="utf8")
    return _path


def record_message(msg):
    file = open(path, "a", encoding="utf8")
    for line in msg.split("\n"):
        file.write(f"[{get_time()}] {line}\n")
    file.close()


path = create_file()
