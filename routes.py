from flask import abort
from requests import get
from appconfig import app


inMemoryDb = {}  # add read from database


@app.route('/<app_name>')
def proxy(app_name):
    url = inMemoryDb.get(app_name)

    if url:
        response = get(url, stream=True)
        return (response.text,
                response.status_code,
                response.headers.items())

    abort(404)
