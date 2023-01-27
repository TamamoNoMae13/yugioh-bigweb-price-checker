import json
import requests

YUGIPEDIA_URL = 'https://yugipedia.com/api.php'
ENGLISH_NAME = 'English name'
JAPANESE_BASE_NAME = 'Japanese base name'
JAPANESE_KANA_NAME = 'Japanese kana name'


def get_card_from_yugipedia(passcode):
	param0 = f'?action=ask&query=[[Password::{passcode}]]'
	param1 = f"|?{ENGLISH_NAME.replace(' ','_')}"
	param2 = f"|?{JAPANESE_BASE_NAME.replace(' ','_')}"
	param3 = f"|?{JAPANESE_KANA_NAME.replace(' ','_')}"

	endpoint = f'{YUGIPEDIA_URL}{param0}{param1}{param2}{param3}&api_version=3&format=json'
	response = requests.get(endpoint)
	response_json = json.loads(response.text)

	result_orig = response_json.get("query").get("results")

	if len(result_orig) == 0:
		return None

	result = list(result_orig[0].values())[0].get('printouts')

	name_en = result.get(ENGLISH_NAME)[0]

	tmp = result.get(JAPANESE_BASE_NAME)
	if len(tmp) == 0:
		name_ja_base = None
	else:
		name_ja_base = tmp[0].replace(' ', '　')

	tmp = result.get(JAPANESE_KANA_NAME)
	if len(tmp) == 0:
		name_ja_kana = None
	else:
		name_ja_kana = tmp[0].replace(' ', '　')

	return name_en, name_ja_base, name_ja_kana
