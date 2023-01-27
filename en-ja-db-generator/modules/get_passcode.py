import os

from values.constants import *


def read_folder_contents():
	"""
		Get all cards' passcode from filenames in EDOPro's script folder.

		Return a list of YGO cards' passcode with 0-padding
		May contains some made-up ID, e.g. the original Egyptian Gods, ...
	"""
	filenames = os.listdir(CARDS_SCRIPT_PATH)
	passcodes = []
	for name in filenames:
		if '.lua' in name:
			passcode = name[1:(len(name) - 4)]
			passcodes.append(passcode.zfill(8))
	passcodes.sort()
	return passcodes


def write_to_passcode_file(arr):
	"""
		Save the result of the above function to a text file when needed.
	"""
	f = open(FILE_HOLDING_PASSCODE_PATH, "w")
	for line in arr:
		f.write(f'{line}\n')
	f.close()
