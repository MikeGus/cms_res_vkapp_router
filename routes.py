from flask import Flask, abort
from requests import get

app = Flask(__name__)

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
