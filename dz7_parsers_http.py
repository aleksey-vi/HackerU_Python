import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup


# На каком сайте искать изображение
TARGET_URL = "https://cyber-ed.ru/"
# Название искомого файла на странице сайта
needle_image = "CyberEd_logo_black-1.png"


def get_body():
    """ Функция получения содержимого страницы для дальнейшего парсинга
    """
    r = requests.get(TARGET_URL)
    r.raise_for_status()  # Кинуть Exception в случае, если страница возвращает код ответ отличный от 200
    return r.text  # Возвращаем текст, а не байты


def get_image_url(html_doc):
    """ Функция поиска искомой картинки в содердимом страницы
    """
    # Инициализируем bs4, в качестве первого аргумента передаем содержимое страницы
    soup = BeautifulSoup(html_doc, 'lxml')

    # Ищем все теги meta со свойством og:image
    # Почему именно meta и почему свойство og:image ?
    # Для того что бы понять откуда забирарать картинку и что вообще парсить
    # Нужно открыть сайт из описания ДЗ, открыть исходный код страницы (правая кнопка мыши, Просмотр кода страницы)
    # И ищем нужную нам картинку
    # Видим что ссылка на картинку лежит в теге meta в атрибуте content
    meta_tags = soup.find_all('meta', property="og:image")

    # Ссылка на скачивание картинки, по-умолчанию None
    download_url = None

    for meta_tag in meta_tags:
        # Если атрибут content у тега meta заканчивается с названием искомого файла
        # то это наш кондидат, мы нашли ссылку по которой будем качать картинку
        if meta_tag['content'].endswith(needle_image):
            # Перезаписываем переменную объявленную выше
            download_url = meta_tag['content']
            break

    return download_url  # Возвращаем ссылку на скачивание


def get_image_content(url):
    """ Функция скачивания картинки
        Возвращает картинку в бинарном виде
    """
    r = requests.get(url)
    r.raise_for_status()  # Кинуть Exception в случае, если страница возвращает код ответ отличный от 200
    return r.content


def parse_args():
    """ Функция парсинга аргументов
    """
    parser = argparse.ArgumentParser("Downloading CyberEd Logo")
    parser.add_argument("-f", "--file", required=True, help="Filename")
    parser.add_argument("-d", "--dir", required=True, help="Saving directory")

    return parser.parse_args()


def main():
    options = parse_args()
    
    filename = options.file
    save_dir = options.dir

    body = get_body()  # Получаем содержимое страницы
    url = get_image_url(body)  # Получаем ссылку на скачивание картинки
    image = get_image_content(url)  # грузим картинку, по-сути в image у нас лежит картинка, пока мы храним ее в ОЗУ

    if not image:  # Если функция вернула None, это означает что искомая картинка не была найдена
        raise Exception('Image is empty!')

    if not os.path.isdir(save_dir):  # Проверяем существует ли папка для сохранения картинок
        os.makedirs(save_dir, 0o755)  # Если нет, создаем путь рекурсивно с правами на папку 755

    # Открываем файл на бинарную запись и сохраняем картинку
    with open(os.path.join(save_dir, filename), "wb") as fp:
        fp.write(image)

# точка входа
if __name__ == "__main__":
    main()

