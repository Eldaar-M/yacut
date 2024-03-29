from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap

NAME_EXSISTS_PHRASE = 'Предложенный вариант короткой ссылки уже существует.'
LINK_IS_READY_PHARASE = 'Ваша новая ссылка готова:'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_url = form.custom_id.data
        if URLMap.query.filter_by(short=short_url).first():
            flash(NAME_EXSISTS_PHRASE.format(short_link=short_url))
            return render_template('index.html', form=form)
        if not short_url:
            short_url = URLMap.get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short_url
        )
        db.session.add(url_map)
        db.session.commit()
        flash(LINK_IS_READY_PHARASE)
        return render_template(
            'index.html',
            form=form,
            url=url_for('redirect_view', short_id=short_url, _external=True)
        )
    return render_template('index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)
