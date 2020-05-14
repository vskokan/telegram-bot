def parse_insertion(text):
    if text.startswith("Фильм ") or text.startswith("фильм ") or text.startswith("Книга ") or text.startswith("книга "):
        new_text = text.split(" ", 1)
        category = new_text[0].capitalize()
        name = new_text[1]
        return(category, name)
    else:
        return 0

def parse_deletion(text):
    if text.startswith("Посмотрел") or text.startswith("посмотрел") or text.startswith("просмотрено") or text.startswith("Просмотрено"):
        new_text = text.split(" ", 1)
        category = 'Фильм'
        name = new_text[1]
        return(category, name)
    if text.startswith("Прочитал") or text.startswith("прочитал") or text.startswith("прочитано") or text.startswith("Прочитано"):
        new_text = text.split(" ", 1)
        category = 'Книга'
        name = new_text[1]
        return(category, name)
    return 0

def parse_deletion_by_name_only(text):
    if text.startswith("Удалить ") or text.startswith("удалить "):
        new_text = text.split(" ", 1)
        name = new_text[1]
        return name
    return 0

def parse_category(text):
    book = ["Книги", "книги", "книга", "Книга"]
    film = ["Фильмы", "фильмы", "фильм", "Фильм"]
    if text in book:
        category = 'Книга'
        return category
    if text in film:
        category = 'Фильм'
        return category
    return 0

def parse_query_to_random_item(text):
    to_read = ["Что почитать", "что почитать","Почитать", "почитать", "что почитать?", "Что почитать?"]
    to_watch = ["Что посмотреть", "что посмотреть","Посмотреть", "посмотреть", "что посмотреть?", "Что посмотреть?"]
    if text in to_read:
        category = 'Книга'
        return category
    if text in to_watch:
        category = 'Фильм'
        return category
    return 0