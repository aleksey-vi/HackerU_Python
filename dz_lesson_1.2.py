# пользователь вводит три числа, выведите эти числа на экран в порядке убывания
# сортировку и подобные функции не используем 

a = int(input("Введите число 1: "))
b = int(input("Введите число 2: "))
c = int(input("Введите число 3: "))

d_list = [a, b, c]

for i in range(len(d_list)): #тут получаем индексы списка
    for j in range(i + 1, len(d_list)): # тут точно такие же индексы но только + 1

        if d_list[i] > d_list[j]: #если элемент в списке d_list[i] больше d_list[j]
            d_list[i], d_list[j] = d_list[j], d_list[i] # меняем их местами


print(d_list[::-1]) #конструкция [::-1] сортирует нам в порядке убывания

