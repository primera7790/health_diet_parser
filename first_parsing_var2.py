import requests
from bs4 import BeautifulSoup
import json
import csv

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
#
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('index.html', 'w', encoding='utf8') as file:
#     file.write(src)

# with open('index.html', encoding='utf8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# categories_href = soup.find_all(class_='mzr-tc-group-item-href')
#
# all_categories_dict = {}
# for item in categories_href:
#     category_name = item.text
#     category_url = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[category_name] = category_url
#
# with open('all_category_dict.json', 'w', encoding='utf8') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open('all_category_dict.json', encoding='utf8') as file:
    all_categories = json.load(file)

count = 1
for category_name, category_href in all_categories.items():
    if count == 1:
        rep = [',', "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '')
        rep = [' ', '-']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        # with open(f'data/{count}_{category_name}.html', 'w', encoding='utf8') as file:
        #     file.write(src)

        with open(f'data/{count}_{category_name}.html', encoding='utf8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
        # product = table_head[0].text
        # calories = table_head[1].text
        # proteins = table_head[2].text
        # fats = table_head[3].text
        # cabohydrates = table_head[4].text

        with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    table_head[0].text,
                    table_head[1].text,
                    table_head[2].text,
                    table_head[3].text,
                    table_head[4].text
                )
            )

        products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
        for item in products_data:
            products_tds = item.find_all('td')

            # title = products_tds[0].find('a').text
            # calories = products_tds[1].text
            # proteins = products_tds[2].text
            # fats = products_tds[3].text
            # carbohydrates = products_tds[4].text

            with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        products_tds[0].find('a').text,
                        products_tds[1].text,
                        products_tds[2].text,
                        products_tds[3].text,
                        products_tds[4].text
                    )
                )



        count += 1

