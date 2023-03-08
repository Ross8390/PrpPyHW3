import re
from bs4 import BeautifulSoup
from fake_headers import Headers
import requests
import json

headers = Headers(os='random', browser='random')
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
new_list = []
vac_list = []


def pars_vacancy_tags(vacancy_tag):
    vacancy_links = vacancy_tag.find('a', class_='serp-item__title')['href']
    try:
        salary = vacancy_tag.find('span', attrs={'data-qa': "vacancy-serp__vacancy-compensation"}).text. \
            replace('\u202f', ' ')
    except AttributeError:
        salary = 'Не указана'
    name = vacancy_tag.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.replace('\xa0', ' ')
    city = vacancy_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.replace('\xa0', ' ')
    description = vacancy_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
    return {
        'url': vacancy_links,
        'salary': salary,
        'name': name,
        'city': city,
        'description': description
    }


def record_json(vac):
    with open('vacancy.json', 'w', encoding='utf-8') as v:
        json.dump(vac, v, ensure_ascii=False)


def find():
    html = requests.get(url, headers=headers.generate())
    soup = BeautifulSoup(html.text, features='lxml')
    vacancy_tags = soup.find_all('div', class_='serp-item')
    for vacancy in vacancy_tags:
        parsed = pars_vacancy_tags(vacancy)
        for i in parsed.values():
            pattern1 = re.search(r'[Dd]jango', i)
            pattern2 = re.search(r'[Ff]lask', i)
            if pattern1 or pattern2:
                new_list.append(parsed)
    for vac in new_list:
        vac.pop('description')
        vac_list.append(vac)
    record_json(vac_list)


if __name__ == '__main__':
    find()