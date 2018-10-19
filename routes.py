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
    infoApp = get_info_app(app_name) 

    if infoApp:
        url = infoApp[1] + ":" + str(infoApp[2])
        print(url)
        response = get(url, stream=True)
        return (response.text,
                response.status_code,
                response.headers.items())

    abort(404)

@app.route('/<app_name>/<path:subpath>')
def proxy(app_name, subpath):
    #url = inMemoryDb.get(app_name)
    infoApp = get_info_app(app_name) 

    if infoApp:
        url = infoApp[1] + ":" + str(infoApp[2]) + '/' + app_name + '/' + subpath
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
    appName = data["appName"]
    if appName is None:
        abort(404)
    infoApp = get_info_app(appName)
    if infoApp is None:
        port, containerId = start_new_docker(appName)
        set_info_app(appName, url_host, port, containerId)
    else:
        res = restart_docker(appName, infoApp[3])
        if res != 0:
            port, containerId = res
            update_info_app(appName, url_host, port, containerId)
    return "OK", 200
