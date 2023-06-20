import sqlite3
import csv

# установка соединения с базой данных
conn = sqlite3.connect("duellio.db")
cursor = conn.cursor()

# создание таблицы
cursor.execute(
    "CREATE TABLE IF NOT EXISTS "
    "situations "
    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
    "Name TEXT(255), "
    "Content TEXT, "
    "rating INTEGER, "
    "situation_type INTEGER DEFAULT (0));"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS "
    " tags ("
    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
    "situation INTEGER,"
    "Name TEXT(128),"
    "CONSTRAINT tags_FK FOREIGN KEY (situation) REFERENCES situations(ID));"
)

data = cursor.execute("SELECT Name FROM situations WHERE situation_type = 0;")
names = [name[0] for name in data.fetchall()]

updated = 0

# чтение файла csv и вставка данных в таблицу
with open("situatsii.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # пропуск заголовка
    for row in reader:
        if row[1] in names:
            continue
        content = row[2]
        pos = content.find(
            "Записи управленческих поединков по данной ситуации:"
        )
        if pos >= 0:
            content = content[:pos]
        content = content.replace('"', '""')
        cmd = f'INSERT INTO situations (Name, Content, rating, situation_type) VALUES("{row[1]}", "{content}", 0, 0);'
        cursor.execute(cmd)
        updated += 1

data = cursor.execute("SELECT Name FROM situations WHERE situation_type = 1;")
names = [name[0] for name in data.fetchall()]

with open("ekspress-situatsii.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # пропуск заголовка
    for row in reader:
        if row[1] in names:
            continue
        content = row[2]
        content = content.replace('"', '""')
        cmd = f'INSERT INTO situations (Name, Content, rating, situation_type) VALUES("{row[1]}", "{content}", 0, 1);'
        cursor.execute(cmd)
        updated += 1


with open("tags.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # пропуск заголовка
    for row in reader:
        name = row[0].replace('"', '""')
        req_result = cursor.execute(f'SELECT id FROM situations WHERE name = "{name}" and situation_type = {row[1]};')
        data = req_result.fetchall()
        situation_id = data[0][0]
        cmd = f'INSERT INTO tags (situation, name) VALUES({situation_id}, "{row[2]}");'
        cursor.execute(cmd)
        updated += 1

# сохранение изменений
conn.commit()

# закрытие соединения
conn.close()

print(f"updated {updated}")
