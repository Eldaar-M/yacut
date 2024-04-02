from datetime import datetime
import random
import re

from flask import url_for

from yacut import db
from settings import (
    ALLOWED_SYMBOLS,
    GENERATION_NUMBER,
    MAX_SHORT_SIZE,
    MAX_ORIGINAL_SIZE,
    REDIRECT_FUNCTION_NAME,
    URL_SYMBOLS_REGEXP
)


ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_SIZE), nullable=False)
    short = db.Column(db.String(MAX_SHORT_SIZE), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_FUNCTION_NAME, short=self.short, _external=True
            )
        )

    @staticmethod
    def get_unique_short_id():
        unique_short = ''.join(
            random.choices(
                ALLOWED_SYMBOLS,
                k=GENERATION_NUMBER
            )
        )
        if not URLMap.get_url(unique_short):
            return unique_short
        else:
            URLMap.get_unique_short_id()

    @staticmethod
    def url_validate(short):
        if (len(short) > MAX_SHORT_SIZE or not re.match(URL_SYMBOLS_REGEXP, short)):
            raise ValueError(INVALID_NAME)
        if URLMap.get_url(short):
            raise ValueError(ALREADY_EXISTS)

    @staticmethod
    def get_url(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_url(original, short):
        if short:
            URLMap.url_validate(short)
        if short is None or short == '':
            short = URLMap.get_unique_short_id()
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url
