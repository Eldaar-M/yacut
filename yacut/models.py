from datetime import datetime
import random
import string

from flask import url_for

from yacut import db

from settings import GENERATION_NUMBER


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_unique_short_id():
        return ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=GENERATION_NUMBER
            )
        )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short_id=self.short, _external=True
            )
        )
