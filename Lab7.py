import random
import hashlib
import json
import os

hash_file = "password_hash.json"

def save_hash(h):
    with open(hash_file, "w") as f:
        json.dump({"hash": h}, f)

def load_hash():
    with open(hash_file, "r") as f:
        return json.load(f)["hash"]

def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

print("=== Парольная защита - Выборка символов ===")
print()

# если пароля ещё нет - регистрация
if not os.path.exists(hash_file):
    print("Первый запуск. Установите пароль.")
    password = input("Введите пароль: ")
    save_hash(get_hash(password))
    password_len = len(password)

    # сохраняем длину пароля тоже (она нужна для выбора позиций)
    with open(hash_file, "w") as f:
        json.dump({"hash": get_hash(password), "len": password_len}, f)

    print("Пароль установлен!")
    print()
else:
    with open(hash_file, "r") as f:
        data = json.load(f)
    password_len = data["len"]
    stored_hash = data["hash"]

print(f"Длина пароля: {password_len} символов")
print()

max_attempts = 3
attempts = 0
access = False

while attempts < max_attempts:
    positions = sorted(random.sample(range(password_len), 3))

    print(f"Попытка {attempts + 1} из {max_attempts}")
    print(f"Введите символы на позициях: {[p + 1 for p in positions]} (нумерация с 1)")

    user_input = input("Ваш ответ (без пробелов): ")

    if len(user_input) != 3:
        print("Нужно ввести ровно 3 символа!")
        continue

    # восстанавливаем пароль частично - нам нужно проверить
    # но мы не знаем остальные символы...
    # поэтому просим пользователя ввести пароль целиком отдельно
    # и проверяем его хэш, а потом проверяем что на нужных позициях
    # стоят введённые символы

    full_input = input("Введите пароль полностью для проверки: ")

    # проверяем хэш полного пароля
    if get_hash(full_input) != stored_hash:
        print("Неверно")
        attempts += 1
        print()
        continue

    # проверяем что символы на нужных позициях совпадают
    correct = True
    for idx, pos in enumerate(positions):
        if full_input[pos] != user_input[idx]:
            correct = False
            break

    if correct:
        print("Доступ разрешён")
        access = True
        break
    else:
        print("Неверно")
        attempts += 1
        print()

if not access:
    print("Слишком много попыток. Доступ заблокирован.")