from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_ORIGINAL_SIZE, MAX_SHORT_SIZE, SHORT_SYMBOLS_REGEXP

ADD_ORIGINAL_PHRASE = 'Добавьте вашу длинную ссылку'
REQUIED_FIELD_PHRASE = 'Обязательное поле'
ADD_SHORT_PHRASE = 'Введите ваш вариант короткой ссылки'
CREATE_PHRASE = 'Создать'
REGEXP_PHRASE = (
    'Можно использовать только большие и маленькие'
    'латинские буквы, цифры в диапазоне от 0 до 9.'
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ADD_ORIGINAL_PHRASE,
        validators=[
            DataRequired(message=REQUIED_FIELD_PHRASE),
            Length(max=MAX_ORIGINAL_SIZE)
        ]
    )
    custom_id = StringField(
        ADD_SHORT_PHRASE,
        validators=[
            Length(max=MAX_SHORT_SIZE),
            Optional(),
            Regexp(
                SHORT_SYMBOLS_REGEXP,
                message=(REGEXP_PHRASE)
            )
        ]
    )
    submit = SubmitField(CREATE_PHRASE)
