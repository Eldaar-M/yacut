from http import HTTPStatus
from flask import abort, flash, redirect, render_template, url_for

from settings import REDIRECT_FUNCTION_NAME
from yacut.error_handlers import GenerationError
from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            url=url_for(
                REDIRECT_FUNCTION_NAME,
                short=URLMap.create(form.original_link.data,
                                    form.custom_id.data,
                                    validate=False).short,
                _external=True
            )
        )
    except (ValueError, GenerationError) as error:
        flash(error)
        return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
