def parseInsertion(text):
    if text.startswith("Фильм ") or text.startswith("фильм ") or text.startswith("Книга ") or text.startswith("книга "):
        newtext = text.split(" ", 1)
        contentType = newtext[0].capitalize()
        contentName = newtext[1]
        return(contentType, contentName)
    else:
        return 0

def parseDeletion(text):
    if text.startswith("Удалить ") or text.startswith("удалить "):
        newtext = text.split(" ", 1)
        contentName = newtext[1]
        return(contentName)
    else:
        return 0

