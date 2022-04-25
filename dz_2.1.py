# дана строка "abhcdefg"
# найдите самую "большую" букву в этой строке и ее индекс

s = "mama mila ramy"
i = 0
N = len(s)
index = -1

while i < N:

    if s[i] == "r":
        index = i
        break
    i += 1

print("index=", index)

