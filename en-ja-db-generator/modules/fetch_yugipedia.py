import json
import requests

YUGIPEDIA_URL = 'https://yugipedia.com/api.php'
ENGLISH_NAME = 'English name'
JAPANESE_BASE_NAME = 'Japanese base name'
JAPANESE_KANA_NAME = 'Japanese kana name'


def get_card_from_yugipedia(passcode):
	try_count = 0

	param0 = f'?action=ask&query=[[Password::{passcode}]]'
	param1 = f"|?{ENGLISH_NAME.replace(' ', '_')}"
	param2 = f"|?{JAPANESE_BASE_NAME.replace(' ', '_')}"
	param3 = f"|?{JAPANESE_KANA_NAME.replace(' ', '_')}"

	endpoint = f'{YUGIPEDIA_URL}{param0}{param1}{param2}{param3}&api_version=3&format=json'

	response = requests.get(endpoint)
	try_count += 1
	while try_count < 3:
		if response.status_code == 200:
			break
		else:
			try_count += 1
			response = requests.get(endpoint)
	if try_count >= 3 and response.status_code != 200:
		return response.status_code

	response_json = json.loads(response.text)

	result_orig = response_json.get("query").get("results")

	if len(result_orig) == 0:
		return None

	result = list(result_orig[0].values())[0].get('printouts')

	name_en = result.get(ENGLISH_NAME)[0]

	tmp1 = result.get(JAPANESE_BASE_NAME)
	if len(tmp1) == 0:
		name_ja_base = None
	else:
		tmp1 = tmp1[0]
		name_ja_base = tmp1.replace(' ', '　')

	tmp2 = result.get(JAPANESE_KANA_NAME)
	if len(tmp2) == 0:
		name_ja_kana = None
	else:
		tmp2 = tmp2[0]
		if tmp2 == tmp1:
			name_ja_kana = None
		else:
			name_ja_kana = tmp2.replace(' ', '　')

	return name_en, name_ja_base, name_ja_kana
