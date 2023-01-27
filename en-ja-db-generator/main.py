from datetime import datetime

from modules.fetch_yugipedia import *


if __name__ == '__main__':
	print(f'Start the program at {datetime.now()}')
	print(get_card_from_yugipedia('00295517'))
