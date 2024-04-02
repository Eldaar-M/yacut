from flask import abort, flash, redirect, render_template, url_for

from settings import REDIRECT_FUNCTION_NAME
from . import app
from .forms import URLMapForm
from .models import URLMap

NAME_EXSISTS_PHRASE = 'Предложенный вариант короткой ссылки уже существует.'
ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    try:
        url_map = URLMap.create_url(form.original_link.data, short)
    except ValueError as error:
        flash(error)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        url=url_for(
            REDIRECT_FUNCTION_NAME,
            short=url_map.short,
            _external=True
        )
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    url_map = URLMap.get_url(short)
    if url_map:
        return redirect(url_map.original)
    abort(404)
