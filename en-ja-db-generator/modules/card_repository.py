import sqlite3
from sqlite3 import Error

from values.constants import *

TABLE_CARDS_NAME = 't_cards'
T_CARDS_COLUMN_PASSCODE_COLUMN = 'passcode'
T_CARDS_COLUMN_NAME_EN = 'name_en'
T_CARDS_COLUMN_NAME_JA = 'name_ja'
T_CARDS_COLUMN_NAME_JA_KANA = 'name_ja_kana'
T_CARDS_COLUMN_LAST_UPDATE = 'last_update'


def create_connection():
	conn = None
	try:
		conn = sqlite3.connect(DB_FILE)
	except Error as e:
		print(e)

	return conn


def search_card(conn: sqlite3.Connection, passcode):
	sql = f'SELECT * FROM `{TABLE_CARDS_NAME}` WHERE `{T_CARDS_COLUMN_PASSCODE_COLUMN}` = ?;'

	cur = conn.cursor()
	cur.execute(sql, (passcode,))

	rows = cur.fetchall()
	if len(rows) != 0:
		return rows[0]

	return None


def insert_card(conn: sqlite3.Connection, card_info):
	sql = f'''INSERT INTO `{TABLE_CARDS_NAME}`
	(`{T_CARDS_COLUMN_PASSCODE_COLUMN}`,
	`{T_CARDS_COLUMN_NAME_EN}`,
	`{T_CARDS_COLUMN_NAME_JA}`,
	`{T_CARDS_COLUMN_NAME_JA_KANA}`,
	`{T_CARDS_COLUMN_LAST_UPDATE}`)
	VALUES(?,?,?,?,?)
	'''

	cur = conn.cursor()
	cur.execute(sql, card_info)
	conn.commit()

	return cur.lastrowid


def update_card(conn: sqlite3.Connection, passcode, card_info: tuple):
	sql = f'''UPDATE {TABLE_CARDS_NAME}
	SET {T_CARDS_COLUMN_NAME_EN}=?,
	{T_CARDS_COLUMN_NAME_JA}=?,
	{T_CARDS_COLUMN_NAME_JA_KANA}=?,
	{T_CARDS_COLUMN_LAST_UPDATE}=?
	WHERE {T_CARDS_COLUMN_PASSCODE_COLUMN}=?
	'''

	card_info_list = list(card_info)
	card_info_list.append(passcode)

	cur = conn.cursor()
	cur.execute(sql, tuple(card_info_list))
	conn.commit()
