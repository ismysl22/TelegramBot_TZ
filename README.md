# TelegramBot_TZ 
## Описание

Тестовое задание. Person Telegram Bot отправляющий следующие сообщения:

через 10 минут - "Добрый день!"

через 90 минут - "Подготовила для вас материал"

Сразу после - Отправка любого фото

Через 2 часа, если не найден в истории сообщений триггер "Хорошего дня" -	"Скоро вернусь с новым материалом!"

Отправляет список зарегистрировавшихся сегодня пользователей по команде /users_today


## Установка
1. Скачайте репозиторий:
```
https://github.com/ismysl22/TelegramBot_TZ
```
2. Активируйте venv и установите зависимости:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Создайте в корневой директории файл .env со следующим наполнением:
```
api_id = аpi_id person telegram
api_hash = 'api_hash person telegram'
```
```
4. Проект готов к запуску.

### Автор
Мыслицкий Илья

imyslitsky22@yandex.ru
