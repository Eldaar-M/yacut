from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

ID_NOT_FOUND = 'Указанный id не найден'
REQUEST_BODY_MISSING = 'Отсутствует тело запроса'
URL_REQUIERD_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
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
    short = data.get('custom_id', None)
    try:
        return jsonify(
            URLMap.create(data['url'], short).to_dict()
        ), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(f'{error}')
