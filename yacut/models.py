from datetime import datetime
import random
import re

from flask import url_for

from yacut import db
from settings import (
    ALLOWED_SYMBOLS,
    SHORT_SIZE,
    MAX_SHORT_SIZE,
    MAX_ORIGINAL_SIZE,
    NUMBER_OF_REPETITIONS,
    REDIRECT_FUNCTION_NAME,
    SHORT_SYMBOLS_REGEXP
)


ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
FAILED_GENERATE = 'Автоматически сгенерировать короткую ссылку не удалось.'
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
    def get_unique_short():
        for i in range(NUMBER_OF_REPETITIONS):
            short = ''.join(
                random.choices(
                    ALLOWED_SYMBOLS,
                    k=SHORT_SIZE
                )
            )
            if not URLMap.get(short):
                return short
        raise ValueError(FAILED_GENERATE)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short):
        if short:
            if (
                (len(short) > MAX_SHORT_SIZE or not
                 re.match(SHORT_SYMBOLS_REGEXP, short))
            ):
                raise ValueError(INVALID_NAME)
            if URLMap.get(short):
                raise ValueError(ALREADY_EXISTS)
        if short is None or short == '':
            short = URLMap.get_unique_short()
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url
