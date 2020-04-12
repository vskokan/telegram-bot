# Сюда можно кидать куски кода с объяснением, что они делают (будет удобно для отчетов)

## Например
Тут импортируем всякие нужные штуки
```python
from telegram.ext import Updater, MessageHandler
from telegram.ext import Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
```
Тут настраиваем прокси
```python
REQUEST_KWARGS = {
    'proxy_url': 'socks5://82.223.120.213:1080',
}
```
Тут использование токена и прокси
```python
updater = Updater(token='1189380390:AAGtbHYKIv_HDlGy4qyaOQ3ukB2GNyY_osE', use_context=True,
                  request_kwargs=REQUEST_KWARGS)
```
