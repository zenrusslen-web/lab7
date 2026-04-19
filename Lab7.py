import hashlib
import json
import os
import random

FILE_NAME = "password_data.json"
MAX_TRIES = 3


def make_hash(symbol, position, salt):
    text = symbol + str(position) + salt
    return hashlib.sha256(text.encode()).hexdigest()


print("Регистрация")
password = input("Придумайте пароль: ")

salt = str(random.randint(1000, 9999))
hashes = []

for i in range(len(password)):
    h = make_hash(password[i], i, salt)
    hashes.append(h)

data = {
    "length": len(password),
    "salt": salt,
    "hashes": hashes
}

with open(FILE_NAME, "w", encoding="utf-8") as f:
    json.dump(data, f)

print("Пароль сохранен")


print("\nВход")

with open(FILE_NAME, "r", encoding="utf-8") as f:
    data = json.load(f)

length = data["length"]
salt = data["salt"]
hashes = data["hashes"]

tries = 0

while tries < MAX_TRIES:
    count = 3
    if length < 3:
        count = length

    positions = random.sample(range(length), count)
    positions.sort()

    ok = True

    for pos in positions:
        user_symbol = input(f"Введите символ пароля {pos + 1}: ")

        if len(user_symbol) != 1:
            print("Нужно вводить ровно один символ")
            ok = False
            break

        user_hash = make_hash(user_symbol, pos, salt)

        if user_hash != hashes[pos]:
            ok = False

    if ok:
        print("Доступ разрешен")
        break
    else:
        tries += 1
        print("Неверные символы пароля")
        print("Осталось попыток:", MAX_TRIES - tries)

if tries == MAX_TRIES:
    print("Доступ заблокирован")