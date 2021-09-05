import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient


# Получение супа, обьеденил два запроса в один
def get_soup(link):
    headers = {
        'User-Agent': 'Mozilla/5.0'}
    response = requests.get(link, headers=headers)
    soup = bs(response.text, 'html.parser')
    return soup


# Функция получает список категорий для последующего извлечения ссылок или списка подкатегорий
def get_catalog_info(link):
    soup = get_soup(link)
    base_soup = soup.find_all('a', attrs={'class': 'catalog__category-item util-hover-shadow'})
    category_info = []
    for i in base_soup:
        category_data = {}
        name = i.find('div', class_='catalog__category-name')
        category_data['name'] = name.getText()
        category_data['url'] = i['href']
        category_info.append(category_data)
    # Не у всех категорий есть подкатегории
    if not category_info:
        return None
    else:
        return category_info


# Функция которая непосредственно парсит наименования, извлекая данные
def get_product_info(link):
    param = '?page='
    soup = get_soup(link)
    pagination = len(soup.findAll('a', class_='page-num'))
    # При финальных тестах я обнаружил, что данные не извлекаются по ссылкам где всего одна страница
    if pagination == 0:
        pagination = 2
    product_info = []
    id = 1
    for page in range(1, pagination):
        print(f'            Сканирование страницы {page} из {pagination - 1}')
        soup = get_soup(link + param + str(page))
        base_soup = soup.findAll('a', attrs={'class': 'block-product-catalog__item'})
        for i in base_soup:
            product_data = {}
            name = i.find('div', class_='product__item-link')
            # Проверка на наличие рейтинга (зеленого либо желтого) Товары из черного списка не учитываются при сборе
            rating_total = i.find('div', attrs={'class': 'rate green rating-value'})
            if rating_total is None:
                rating_total = i.find('div', attrs={'class': 'rate violation-value'})
            if rating_total is None:
                break
            rating_block = i.find('div', class_='rating-block')
            rating_values = []
            try:
                for n in rating_block:
                    if n == '\n':
                        continue
                    else:
                        rating_values.append(n.find('div', class_='right').getText())
                product_data['_id'] = id
                id += 1
                product_data['Название'] = name.getText()
                product_data['Общий рейтинг'] = int(rating_total.getText())
                product_data['Безопасность'] = int(rating_values[0])
                product_data['Натуральность'] = int(rating_values[1])
                product_data['Пищевая ценность'] = int(rating_values[2])
                # Не у всех товаров есть этот параметр
                try:
                    product_data['Качество'] = int(rating_values[3])
                except:
                    product_data['Качество'] = 'None'
                product_info.append(product_data)
            except:
                continue
    return product_info


url = 'https://roscontrol.com'
catalog = get_catalog_info(url + '/category/produkti/')

client = MongoClient('127.0.0.1', 27017)
client.drop_database('Products')
db = client['Products']

for i in catalog:
    print('Поиск в категории {}...'.format(i['name']))
    subcatalog = get_catalog_info(url + i['url'])
    try:
        for n in subcatalog:
            print('     Поиск в подкатегории {}...'.format(n['name']))
            collection = db[n['name']]
            category_data = get_product_info(url + n['url'])
            try:
                collection.insert_many(category_data)
            except:
                continue

    except:
        collection = db[i['name']]
        category_data = get_product_info(url + i['url'])
        collection.insert_many(get_product_info(url + i['url']))
