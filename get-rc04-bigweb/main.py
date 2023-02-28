from modules.fetch_card import *
import time

if __name__ == '__main__':
	print('SetID,Name,Foil,Condition,Price')
	for i in range(1, 81):
		get_result_from_set_id(f'RC04-JP{str(i).zfill(3)}')
		time.sleep(3)
