import sqlite3

from modules.access import get_epoch_now

TABLE_CARDS_NAME = 't_cards'
T_CARDS_COLUMN_PASSCODE_COLUMN = 'passcode'
T_CARDS_COLUMN_NAME_EN = 'name_en'
T_CARDS_COLUMN_NAME_JA_BASE = 'name_ja_base'
T_CARDS_COLUMN_NAME_JA_KANA = 'name_ja_kana'
T_CARDS_COLUMN_LAST_UPDATE = 'last_update'


def search_card(conn: sqlite3.Connection, passcode: str):
	sql = f'SELECT * FROM `{TABLE_CARDS_NAME}` WHERE `{T_CARDS_COLUMN_PASSCODE_COLUMN}` = ?;'

	cur = conn.cursor()
	cur.execute(sql, (passcode,))

	rows = cur.fetchall()
	if len(rows) != 0:
		return rows[0]

	return None


def insert_card(conn: sqlite3.Connection, passcode: str, card_info: tuple):
	"""
		:param conn
		:param passcode
		:param card_info: Should contains exactly 3 elements: name_en, name_ja_base, name_ja_kana
	"""

	sql = f'''INSERT INTO `{TABLE_CARDS_NAME}`
		(`{T_CARDS_COLUMN_PASSCODE_COLUMN}`,
		`{T_CARDS_COLUMN_NAME_EN}`,
		`{T_CARDS_COLUMN_NAME_JA_BASE}`,
		`{T_CARDS_COLUMN_NAME_JA_KANA}`,
		`{T_CARDS_COLUMN_LAST_UPDATE}`)
		VALUES(?,?,?,?,?)
	'''
	data = (passcode, card_info[0], card_info[1], card_info[2], get_epoch_now())

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


def update_card(conn: sqlite3.Connection, passcode: str, card_info: tuple):
	"""
		:param conn
		:param passcode
		:param card_info: Should contains exactly 3 elements: name_en, name_ja_base, name_ja_kana
	"""

	sql = f'''UPDATE {TABLE_CARDS_NAME}
		SET {T_CARDS_COLUMN_NAME_EN}=?,
		{T_CARDS_COLUMN_NAME_JA_BASE}=?,
		{T_CARDS_COLUMN_NAME_JA_KANA}=?,
		{T_CARDS_COLUMN_LAST_UPDATE}=?
		WHERE {T_CARDS_COLUMN_PASSCODE_COLUMN}=?
	'''
	data = (card_info[0], card_info[1], card_info[2], get_epoch_now(), passcode)

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()
