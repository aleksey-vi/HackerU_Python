"""дана строка, найдите самую "большую" букву в этой строке и ее индекс.
(буквы в строке это тоже строки и их можно сравнивать, т.е. условие "a" > "g" - валидное. Строки сравниваются в алфавитном порядке.
Например для строки "abhcdefg"самая большая буква это h, а ее индекс - 2.
* найдите вторую "большую" букву в строке. Для строки "abhcdefg" ответ - "g"



s = ("abhcdefg")
max_char = s[0]
id = 0
for i in range(len(s)):
    if max_char < s[i]:
        max_char = s[i]
        id = i

id2 = 0
max_char2 = s[0]
for i in range(len(s)):
    if id == i:
      continue
    if max_char2 < s[i]:
        max_char2 = s[i]
        id2 = i

print("максимальное значение=", max_char)
print("id максимального значения=", id)
print("ПРЕДмаксимальное значение=", max_char2)
print("id ПРЕДмаксимального значения=", id2)
