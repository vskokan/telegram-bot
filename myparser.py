def parseInsertion(text):
    if text.startswith("Фильм ") or text.startswith("фильм ") or text.startswith("Книга ") or text.startswith("книга "):
        newtext = text.split(" ", 1)
        contentType = newtext[0].capitalize()
        contentName = newtext[1]
        return(contentType, contentName)
    else:
        return 0

def parseDeletion(text):
    if text.startswith("Посмотрел") or text.startswith("посмотрел") or text.startswith("просмотрено") or text.startswith("Просмотрено"):
        newtext = text.split(" ", 1)
        contentType = 'Фильм'
        contentName = newtext[1]
        return(contentType, contentName)
    if text.startswith("Прочитал") or text.startswith("прочитал") or text.startswith("прочитано") or text.startswith("Прочитано"):
        newtext = text.split(" ", 1)
        contentType = 'Книга'
        contentName = newtext[1]
        return(contentType, contentName)
    return 0

