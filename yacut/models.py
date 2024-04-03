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
    NUMBER_GENERATION,
    REDIRECT_FUNCTION_NAME,
    SHORT_SYMBOLS_REGEXP
)
from yacut.error_handlers import GenerationError


ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
FAILED_GENERATE = 'Автоматически сгенерировать короткую ссылку не удалось.'
INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
INVALID_ORIGINAL_SIZE = ('Длинная ссылка превышает'
                         ' допустимое количество символов')


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
        for _ in range(NUMBER_GENERATION):
            short = ''.join(random.choices(
                ALLOWED_SYMBOLS,
                k=SHORT_SIZE
            ))
            if not URLMap.get(short):
                return short
        raise GenerationError(FAILED_GENERATE)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short, form=False):
        if not short:
            short = URLMap.get_unique_short()
        if URLMap.get(short):
            raise ValueError(ALREADY_EXISTS)
        if not form:
            if (
                (len(short) > MAX_SHORT_SIZE or not
                 re.match(SHORT_SYMBOLS_REGEXP, short))
            ):
                raise ValueError(INVALID_SHORT_NAME)
            if len(original) > MAX_ORIGINAL_SIZE:
                raise ValueError(INVALID_ORIGINAL_SIZE)
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
