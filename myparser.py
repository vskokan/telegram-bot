def parseText(text):
    if text.startswith("Фильм ") or text.startswith("фильм ") or text.startswith("Книга ") or text.startswith("книга "):
        newtext = text.split(" ", 1)
        contentType = newtext[0].capitalize()
        contentName = newtext[1].capitalize()
        return(contentType, contentName)
    else:
        return 0