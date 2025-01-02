import re
import csv
import unicodedata

import requests

CREATE_SITUATION_API = "http://127.0.0.1:8000/situations/"
UPDATE_TAGS_API = "http://127.0.0.1:8000/tags/"


def make_request_dict(title: str, text: str, standard: bool = True) -> dict:
    return {
        "situation": {
            "title": f"{title}",
            "text": f"{text}",
            "standard": standard,
        },
        "tags": [],
    }


def remove_control_chars(text: str) -> str:
    return "".join(ch for ch in text if unicodedata.category(ch)[0] != "Cc")


def multi_replace(
    text: str, replacements: dict, whole_words_only: bool = False
) -> str:
    if whole_words_only:
        keys = (re.escape(k) for k in replacements.keys())
        pattern = re.compile(r"\b(" + "|".join(keys) + r")\b")
    else:
        pattern = re.compile(
            "|".join(re.escape(k) for k in replacements.keys())
        )
    result = pattern.sub(lambda x: replacements[x.group()], text)
    return result


def convert2html(text: str) -> str:
    repl = {"\n": "<br>", '"': "&quot;", "—": "&mdash;", " ": "&nbsp;"}
    return multi_replace(text, repl)


def add_situations(file_name: str, standard: bool) -> int:
    updated = 0
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # пропуск заголовка
        for row in reader:
            if len(row) < 3:
                continue
            content = row[2]
            pos = content.find(
                "Записи управленческих поединков по данной ситуации:"
            )
            if pos >= 0:
                content = content[:pos]
            title = remove_control_chars(convert2html(row[1]))
            text = remove_control_chars(convert2html(content))
            r = requests.post(
                CREATE_SITUATION_API,
                json=make_request_dict(
                    title=title, text=text, standard=standard
                ),
            )
            if r.status_code == 200:
                updated += 1
            else:
                print(f"error add {title}. {r.status_code}: {r.text}")
    return updated


def update_tags() -> int:
    updated = 0
    with open("tags.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # пропуск заголовка
        for row in reader:
            title = remove_control_chars(convert2html(row[0]))
            standard = row[1] == "0"
            tag = remove_control_chars(convert2html(row[2]))
            situation = make_request_dict(title, "", standard)
            tags = [
                {"name": tag},
            ]
            r = requests.post(
                UPDATE_TAGS_API,
                json=situation | {"tags": tags},
                params={"clear": False},
            )
            if r.status_code == 200:
                updated += 1
            else:
                print(f"{r.status_code}: {r.text}")
    return updated


#updated = add_situations("situatsii.csv", True)
updated = add_situations("situations_kub.csv", True)
print(f"added standard {updated}")
#updated = add_situations("ekspress-situatsii.csv", False)
updated = add_situations("situations_bub.csv", False)
print(f"added express {updated}")

#updated = update_tags()
#print(f"updated tags {updated}")
