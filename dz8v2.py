'''
со страницы https://babybug.ru/brendy/melissa/ собрать данные о всех товарах,
а именно название, цену и картинку
картинки сохранить в папку images/, названия, цены и ссылки на товар в текстовый файл в виде:
название1, цена1, ссылка1
название2, цена2, ссылка2
'''

import os
import re
import requests
from bs4 import BeautifulSoup




BASE_URL = "https://babybug.ru"  # базовый url
page_1 = "/brendy/melissa/"  # первая страница с товарами


def get_melissa_page(url):
    """ Функция возвращаем содержимое страницы
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception:  # если ответ отлинчный от 200, возвращаем bs4 объект с пустой страницей
        return BeautifulSoup('<html></html>', 'lxml')

    soup = BeautifulSoup(r.text, 'lxml')

    return soup


def get_products_per_page(soup):
    """ В данной функции парсим переданную страницу, забираем все товары и возвращаем результат
    """
    products = []  # для начала, объявим пустой результирующий список

    # находим элемент .catalog-list, именно в этом блоке содержатся элементы каталого
    # это сделано для того, что бы не забрать лишние элементы вне каталога
    catalog = soup.find(class_="catalog-list")
    if not catalog:
        # Если на странице нет элемента .catalog-list - возвращаем пустой список
        # иначе говоря, товаров на странице не найдено
        return products

    products_html = catalog.find_all(class_='product-card')  # ищем все элементы каталога
    if not products_html:  # если ни одного элемента не найдено - возвращаем пустой список
        return products

    for product_html in products_html:  # итерируемся по полученным html элементам каталога
        title = product_html.find(class_="product-card__title")  # заголовок
        price = product_html.find(class_="product-card__prices")  # cтоимость
        image = product_html.find(class_="product-card__img")  # картинка
        link = product_html.find("a", class_="product-card__imgs")  # ссылка на сам товар

        product = {}  # инициализируем пустой словарь

        if title:
          # получаем текстовое содержимое html-тега и удаляем пробелы с начала и конца
            product['title'] = title.text.strip()

        if price:
            print(price)
            # Удаляем все не цифровые символы из строки со стоимостью и делаем значение интом
            # дело в том, что если посмотреть текствое содержимое html-тега price.span.text
            # то увидим, что в стоимости есть unicode символ \xa0
            # наша задача избавиться от него, это можно сделать методом .replace у строки
            # далее с помощью регулярных выражений, удаляем все не цифровые символы re.sub('[^0-9]', '', 'asda123ggg')
            # и делаем полученное значение int
            # print(price.span.text)
            product['price'] = int(re.sub('[^0-9]', '', price.span.text.replace(u'\xa0', '')))

        if image:
            # получаем ссылку на изображение из атрибута src у тега с изображением
            product['image_url'] = image['src']

        if link:
            # полуаем ссылку на товар из тега <a> и атрибута href
            product['url'] = f"{BASE_URL}{link['href']}"
        # print(product)
        # Добавляем словарь в список
        products.append(product)

    # тут мы ищем на странице есть ли кнопка с переходом на следующую страницу
    # если нет возвращаем кортеж, где первый элемент сам список продуктов со страницы
    # а второй элемент False - означает, что ссылки на следующую страницу нету
    pagination_item_next = soup.find(class_="pagination__item _next")
    if not pagination_item_next:
        return products, False

    # получаем ссылку на следующую страницу с товарами
    next_page = pagination_item_next.a["href"]

    # возвращаем сам список продуктов и ссылку на следующую страницу с товарами
    return products, next_page


def get_image_content(url=None):
    """ Функция скачивания картинки
        Возвращает картинку в бинарном виде
    """
    if not url:  # если не передана ссылка
        return b''  # возвращаем пустую байт строку

    r = requests.get(url)

    r.raise_for_status()  # Кинуть Exception в случае, если страница возвращает код ответ отличный от 200

    return r.content


def collect_products(url):
    """ Почитай коменты к этой функции
        Может не стоит так усложнять, хотя это правильный подход
        есть еще один вариант, но он не правильный
        суть этого варианта такова:
            1. создаем список с ссылками на все страницы каталога
            2. итерируемся по этому списку
            3. получаем все товары со страниц
            Этот вариант плох тем, что мы заранее сами создаем список со всеми ссылками
            А если таких ссылок будет 10/20/50/100 получается нам вручную придется добавлять каждую
            т е это перейти руками в барузере на каждую страницу и скопировать ссылку
            Думаю ты уловил суть :)
    """
    soup = get_melissa_page(url)  # забираем сожержимое страницы
    products, next_page = get_products_per_page(soup)  # получаем список товаров и ссылку на следующую страницу с товарами

    # если ЕСТЬ ссылка на след. страницу
    if next_page:
        # вызываем текущую функцию еще раз но в качестве аргумента передаем ссылу на следующую страницу
        # !!! Функции которые вызывают сами себя называются - рекурсией
        # Важно! что бы в такой функции было условие выхода
        # У нас оно есть, это условие if next_page
        products += collect_products(f"{BASE_URL}{next_page}")

    return products


def main():
    url = f"{BASE_URL}{page_1}"
    products = collect_products(url)

    if not os.path.isdir('images'):
        os.mkdir('images')

    file_content = ''  # объявляем пустую строку, это будет содержимое файла
    for product in products:
        # записываем информацию о продукте в строку, не забываем о символе новой строки ( \n в конце )
        file_content += f"{product['title']}, {product['price']}, {product['url']}\n"

        download_image_url = f"{BASE_URL}/{product['image_url']}"

        # скачиваем картинку
        image_content = get_image_content(download_image_url)

        # заменяем пробелы в строке с заголовком на нижнее подчеркивание
        image_name = product['title'].replace(' ', '_')

        with open(f"images/{image_name}.jpg", "wb") as imgp:  # сохраняем картинку в файл
            imgp.write(image_content)

    with open('products.txt', 'w') as fp:  # открываем файл со вписком товаров на запись
        fp.write(file_content)


if __name__ == "__main__":
    """ Точка входа
    """
    main()
