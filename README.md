# Проект YaCut — сервис укорачивания ссылок
## Технологии

- Python
- Flask
- SQLAlchemy

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Eldaar-M/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Как запустить проект:
Примените миграции:
```
flask db upgrade
```
В коревой директории проекта введите:
```
flask run
```
## API:
- /api/id/ — POST-запрос на создание новой короткой ссылки;
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.
### Автор 
[Эльдар Магомедов](https://github.com/Eldaar-M)