from appconfig import get_db, app


def get_info_app(appName):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "SELECT * FROM Apps WHERE appName=?"
        cursor.execute(sql, [appName])
        return cursor.fetchone()


def set_info_app(appName, url, port, container):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "INSERT INTO Apps VALUES (?, ?, ?, ?)"
        cursor.execute(sql, [appName, url, port, container])
        get_db().commit()


def update_info_app(appName, url, port, container):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "UPDATE Apps SET url = ? , container = ? , port = ? WHERE appName=?"
        cursor.execute(sql, [url, container, port, appName])
        get_db().commit()

