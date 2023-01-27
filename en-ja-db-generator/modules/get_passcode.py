import os

from values.constants import *


def read_folder_contents():
	filenames = os.listdir(CARDS_SCRIPT_PATH)
	arr = []
	for name in filenames:
		if '.lua' in name:
			passcode = name[1:(len(name) - 4)]
			arr.append(passcode.zfill(8))
	arr.sort()
	return arr


def write_to_file(arr):
	f = open(FILE_HOLDING_PASSCODE_PATH, "w")
	for line in arr:
		f.write(f'{line}\n')
	f.close()
