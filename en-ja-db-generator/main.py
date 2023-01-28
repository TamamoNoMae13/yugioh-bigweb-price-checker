import time

from modules.access import *
from modules.card_repository import *
from modules.fetch_yugipedia import get_card_from_yugipedia
from modules.get_passcode import *

if __name__ == '__main__':
	now = get_epoch_now()
	# print('Start searching & writing passcode to file.')
	# write_to_passcode_file(read_folder_contents())
	# print('Finished writing passcode to file.')

	print('Establish connection to SQLite file.')
	conn = create_connection()

	if conn is not None:
		print('Connected.')

		passcodes = get_passcode_from_file()
		failed_passcodes = []
		if passcodes is None or len(passcodes) == 0:
			print('No passcode found.')
		else:
			i = 0
			while len(passcodes) > 0:
				success = True
				code = passcodes[i]
				existed_record = search_card(conn, code)
				if existed_record is None or (type(existed_record) is tuple and get_epoch_now() - existed_record[4] > 86400):
					while get_epoch_now() - now < 2:
						time.sleep(0.125)
					card_names = get_card_from_yugipedia(code)
					now = get_epoch_now()
					if card_names is None:
						print(f'Cannot find on Yugipedia, id: {code}')
					elif type(card_names) is int and 400 <= card_names <= 599:
						print(f'API call error at id: {code}, status: {card_names}')
						success = False
					elif type(card_names) is tuple:
						if existed_record is None:
							insert_card(conn, code, card_names)
							print(
								f'Inserted, id: {code}, en: {card_names[0]}, base: {card_names[1]}, kana: {card_names[2]}')
						elif card_names[0] != existed_record[1] or card_names[1] != existed_record[2] \
							or card_names[2] != existed_record[3]:

							update_card(conn, code, card_names)
							print(f'Updated, id: {code}, en: {card_names[0]}, base: {card_names[1]}, kana: {card_names[2]}')
						else:
							print(f'No change, id: {code}')
					else:
						print(f'Code bullshit, id: {code}')
				else:
					print(f'Trustable cache, ignore id: {code}')

				if success:
					del passcodes[i]
				else:
					i += 1
					if i > len(passcodes):
						i = 0

				print(f'Next in queue: {passcodes[i]}, {passcodes[i+1]}, {passcodes[i+2]}, ... ({len(passcodes)} left)')

		print('Try to close the connection to SQLite file.')
		conn.close()
		print('Finished closing the connection to SQLite file.')
	else:
		print('Failed.')

	print('Job done!')
