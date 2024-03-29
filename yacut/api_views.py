import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import URL_SYMBOLS_REGEXP, MAX_URL_SIZE

ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
ID_NOT_FOUND = 'Указанный id не найден'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
REQUEST_BODY_MISSING = 'Отсутствует тело запроса'
URL_REQUIERD_FIELD = '\"url\" является обязательным полем!'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(REQUEST_BODY_MISSING)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIERD_FIELD)
    short_url = data.get('custom_id', None)
    if short_url:
        if URLMap.query.filter_by(short=short_url).first():
            raise InvalidAPIUsage(ALREADY_EXISTS)
        if len(short_url) > MAX_URL_SIZE or not re.match(
            URL_SYMBOLS_REGEXP,
            short_url
        ):
            raise InvalidAPIUsage(INVALID_NAME)
    else:
        short_url = URLMap.get_unique_short_id()
    url_map = URLMap(
        original=data['url'],
        short=short_url
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
