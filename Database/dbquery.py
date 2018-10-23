from appconfig import get_db, app


def get_info_app(app_name):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "SELECT * FROM Apps WHERE appName=?"
        cursor.execute(sql, [app_name])
        return cursor.fetchone()


def set_info_app(app_name, url, port, container):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "INSERT INTO Apps VALUES (?, ?, ?, ?)"
        cursor.execute(sql, [app_name, url, port, container])
        get_db().commit()


def update_info_app(app_name, url, port, container):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "UPDATE Apps SET url = ? , container = ? , port = ? WHERE appName=?"
        cursor.execute(sql, [url, container, port, app_name])
        get_db().commit()

