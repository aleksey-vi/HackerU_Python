# пользователь вводит два числа, выведите эти числа на экран в порядке убывания

a = int(input("Введите число 1: "))
b = int(input("Введите число 2: "))

my_list = [a, b]
my_list.sort(reverse=True) # True- сортирует в порядке убывания False-в порядке возрастания
print(my_list)

