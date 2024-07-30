from datetime import datetime
import pytz
import os


def get_date():
	return datetime.now(pytz.timezone("Europe/Moscow")).strftime("%D").replace("/", ".")


def create_file():
	path = f"records/{get_date()}.log"
	num = 2
	while os.path.exists(path):
		path = f"records/{get_date()}_{num}.log"
		num += 1
	open(path, "w", encoding="utf8")
	return path


path = create_file()


def record_message(msg):
	file = open(path, "a", encoding="utf8")
	for line in msg.split("\n"):
		file.write(f"[{get_time()}] {line}\n")
	file.close()



def get_time():
	return datetime.now(pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S")