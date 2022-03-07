import requests
from bs4 import BeautifulSoup as bs
import json
from pprint import pprint as pp


def get_soup(link,params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
    response = requests.get(link, headers=headers,params=params)
    soup = bs(response.text, 'html.parser')
    return soup


def page_parse(soup,list):
    for i in soup:
        vacancy_data = {}
        vacancy_data['Название вакансии'] = i.find('a',{'data-qa':'vacancy-serp__vacancy-title'}).text
        vacancy_data['Компания'] = i.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text.replace(u'\xa0',
                                                                                                           u' ')
        salary_info = {}
        try:
            salary_base = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.replace(u'\u202f', u'')
            test = salary_base.split()
            if len(test) == 4:
                salary_info['Минимальная'] = int(test[0])
                salary_info['Максимальная'] = int(test[2])
                salary_info['Валюта'] = test[3]
            elif len(test) == 3:
                if test[0] == 'от':
                    salary_info['Минимальная'] = int(test[1])
                    salary_info['Максимальная'] = None
                    salary_info['Валюта'] = test[2]
                if test[0] == 'до':
                    salary_info['Минимальная'] = None
                    salary_info['Максимальная'] = int(test[1])
                    salary_info['Валюта'] = test[2]
        except:
            salary_info = {None}
        vacancy_data['Зарплата'] = salary_info

        vacancy_url = i.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_data['URL'] = vacancy_url['href']
        list.append(vacancy_data)
    return


full_data = []
page = 1
url = "https://hh.ru"
target = '/search/vacancy'
filter = {
    'area': '1',
    'professional_role':'31'

}

while True:
    print(f'Сканирование страницы {page}')
    soup = get_soup(url+target,filter)
    base_soup = soup.findAll('div',class_='vacancy-serp-item-body')
    full_data.append(page_parse(base_soup,full_data))
    pagination = soup.find('a', {'data-qa': 'pager-next'})
    try:
        next_page = pagination['href']
        target = next_page
        page += 1
    except:
        break

print(f'Готово! Всего обработано вакансий: {len(full_data)}')

with open('task1.json', 'w', encoding='utf-8') as f:
    json.dump(full_data, f, ensure_ascii=False, indent=4)
