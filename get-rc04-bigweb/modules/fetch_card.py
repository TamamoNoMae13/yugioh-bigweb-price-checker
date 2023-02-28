import json
import requests

BIGWEB_API_URL = 'https://api.bigweb.co.jp'
API_PRODUCT_ENDPOINT = '/products'
PARAM_YGO = 'game_id=9'
PARAM_NAME = 'name='


def get_result_from_set_id(set_id: str):
    site = f'{BIGWEB_API_URL}{API_PRODUCT_ENDPOINT}?{PARAM_YGO}&{PARAM_NAME}{set_id}'
    status_code = 0
    response = requests.get(site)

    while response.status_code != 200:
        response = requests.get(site)
        print(f'Retry at {set_id}')

    response_json = json.loads(response.text)

    results = []

    items: list = response_json['items']
    for item in items:
        set_id = item['fname']
        name = item['name']
        rarity = item['rarity']['slip']
        match rarity:
            case 'アルティメット':
                foil = 'UL'
            case 'シークレット':
                foil = 'SE'
            case _:
                foil = rarity
        match item['condition']['web']:
            case 'プレイ用':
                condition = 'Played'
            case 'キズ':
                condition = 'Damaged'
            case _:
                condition = ''
        if item['is_hidden_price']:
            price = -1
        else:
            price = item['price']

        results.append((set_id, name, foil, condition, price))

    for result in results:
        print(f'{result[0]},{result[1]},{result[2]},{result[3]},{result[4]}')
