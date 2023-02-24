from bs4 import BeautifulSoup, ResultSet
import requests


def get_set_and_name(rarity: str, group: ResultSet) -> list:
    result = []

    for block in group:
        set_id_group = block.find('p', class_='id').find('a')
        set_id = set_id_group.get_text().strip()

        card_name_group = block.find('p', class_='name').find('a')
        card_name = card_name_group.get_text().strip()

        if '(イラス' in card_name:
            set_id = f'{set_id}(違)'

        price_group = block.find('p', class_='price')
        price_str = price_group.get_text().strip().replace('円', '')
        price = int(price_str)

        result.append((set_id, card_name, rarity, price))

    return result


def custom_sort_key(k: tuple) -> str:
    return k[0]


if __name__ == '__main__':
    r = requests.get('https://yuyu-tei.jp/game_ygo/sell/sell_price.php?ver=rc04')
    soup = BeautifulSoup(r.text, 'html.parser')

    foil_group = [('HR',   soup.find_all('li', class_='card_unit rarity_HR')),
                  ('QCSE', soup.find_all('li', class_='card_unit rarity_QCSE')),
                  ('EXSE', soup.find_all('li', class_='card_unit rarity_EXSE')),
                  ('SE',   soup.find_all('li', class_='card_unit rarity_SE')),
                  ('UL',   soup.find_all('li', class_='card_unit rarity_UL')),
                  ('CR',   soup.find_all('li', class_='card_unit rarity_CR')),
                  ('UR',   soup.find_all('li', class_='card_unit rarity_UR')),
                  ('SR',   soup.find_all('li', class_='card_unit rarity_SR'))]

    card_list = []
    for foil in foil_group:
        card_list.extend(get_set_and_name(foil[0], foil[1]))
    card_list.sort(key=custom_sort_key)

    with open('price.csv', 'w', encoding='utf8') as f:
        lines = ['SetID,Name,SR,UR,SE,CR,UL,ES,25TH\n']
        previous_id = ''
        current_id = ''
        current_card_name = ''
        qcse = -1
        exse = -1
        ul = -1
        cr = -1
        se = -1
        ur = -1
        sr = -1

        for c in card_list:
            if current_id != c[0]:
                if previous_id != '' or (previous_id == '' and c[0] == 'RC04-JP002'):
                    lines.append(f'{current_id},{current_card_name},{sr},{ur},{se},{cr},{ul},{exse},{qcse}\n')
                    qcse = -1
                    exse = -1
                    ul = -1
                    cr = -1
                    se = -1
                    ur = -1
                    sr = -1

                previous_id = current_id
                current_id = c[0]
                current_card_name = c[1]

            match (c[2]):
                case 'QCSE':
                    qcse = c[3]
                case 'EXSE':
                    exse = c[3]
                case 'SE':
                    se = c[3]
                case 'UL':
                    ul = c[3]
                case 'CR':
                    cr = c[3]
                case 'UR':
                    ur = c[3]
                case 'SR':
                    sr = c[3]

        lines.append(f'{current_id},{current_card_name},{sr},{ur},{se},{cr},{ul},{exse},{qcse}\n')

        f.writelines(lines)
        f.close()
