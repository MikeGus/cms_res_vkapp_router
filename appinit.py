from appconfig import get_db, app

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('Database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()