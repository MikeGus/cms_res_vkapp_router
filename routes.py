import json
from flask import abort, request
from requests import get
from appconfig import app, url_host
from idocker import start_new_docker, restart_docker
from Database.dbquery import get_info_app, set_info_app, update_info_app

#inMemoryDb = {}  # add read from database


@app.route('/<app_name>')
def redirect(app_name):
    #url = inMemoryDb.get(app_name)
    info_app = get_info_app(app_name) 

    if info_app:
        url = info_app[1] + ":" + str(info_app[2])
        print(url)
        response = get(url, stream=True)
        return (response.text,
                response.status_code,
                response.headers.items())

    abort(404)

@app.route('/<app_name>/<path:subpath>')
def proxy(app_name, subpath):
    #url = inMemoryDb.get(app_name)
    info_app = get_info_app(app_name) 

    if info_app:
        url = info_app[1] + ":" + str(info_app[2]) + '/' + app_name + '/' + subpath
        print(url)
        response = get(url, stream=True)
        return (response.text,
                response.status_code,
                response.headers.items())

    abort(404)

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    if data is None:
        abort(400)
    app_name = data["appName"]
    if app_name is None:
        abort(404)
    info_app = get_info_app(app_name)
    if info_app is None:
        port, container_id = start_new_docker(app_name)
        set_info_app(app_name, url_host, port, container_id)
    else:
        port, container_id = restart_docker(app_name, info_app[3], info_app[2])
        update_info_app(app_name, url_host, port, container_id)
    return "OK", 200
