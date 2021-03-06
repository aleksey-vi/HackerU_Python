# дан список айпишников (в виде строк, например "192.168.0.10") из разных под сетей
# a) оставьте в списке только айпишники из сети 192.168.0...
# b) превратите каждый айпишник в кортеж из его октетов в числовом виде, т.е. (192,168,8,1)
# c) отсортируйте полученный список по последнему октету
# программа должна содержать всего три строки:
# 1 исходный список айпишников
# 2 алгоритм по заданию (в одну строку)
# 3 print() с результатом
# ЗЫ: в принципе задание можно сделать и в одну строку целиком.
# ЗЗЫ: пользоваться циклами и отдельно определенными функциями запрещается:)
ip = [
    "192.168.0.1",
    "192.168.0.3",
    "192.168.0.8",
    "192.168.0.56",
    "192.168.0.3", "192.168.0.100", "192.168.0.1", "192.168.10.2"]
answer = sorted( # сортируем по последнему октету ip адреса
    set([ # оставляем только уникальные значения
        tuple(map(lambda x: int(x), i.split('.')))  #  котреж(применяем ко всем элементам
        # анонимную функцию лябда, которая делает каждый элемент типом int, а в качестве второго аргумента передается,
        # формуриемый список из строки, где в качестве разделителя используется точка)
        for i in list( # в данном цикле мы перебираем в переменной i(отсортированные элементы) из списка
            filter(lambda ip: ip.startswith("192.168.0"), ip)  # фультруем все адреса в списке ip которые начинаются с "192.168.0"
        )
    ])
)
# answer = sorted(set([tuple(map(lambda x: int(x), i.split('.'))) for i in list(filter(lambda x: x.startswith("192.168.0"), ip))]))
# настоящая 1 строка)
print(answer)