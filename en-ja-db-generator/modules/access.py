import datetime
import sqlite3
from sqlite3 import Error

from values.constants import DB_FILE, FILE_HOLDING_PASSCODE_PATH


def create_connection():
	conn = None
	try:
		conn = sqlite3.connect(DB_FILE)
	except Error as e:
		print(e)

	return conn


def get_passcode_from_file():
	with open(FILE_HOLDING_PASSCODE_PATH) as f:
		content = f.read().splitlines()

	return content


def get_epoch_now():
	return int(datetime.datetime.now().timestamp())
