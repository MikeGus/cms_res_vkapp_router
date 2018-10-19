import sqlite3
from flask import _app_ctx_stack, Flask

app = Flask(__name__)


DATABASE = 'Database/Apps.db'


def get_db():
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is None:
        db = _app_ctx_stack.top._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('Database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()