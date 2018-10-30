import json
import os
from flask import abort, request
from requests import get
from appconfig import app, url_host, apps_state, AppsState, get_server_key
from idocker import start_new_docker, restart_docker
from Database.dbquery import get_info_app, set_info_app, update_info_app

#inMemoryDb = {}  # add read from database


@app.route('/<app_name>')
def redirect(app_name):
    #url = inMemoryDb.get(app_name)
    info_app = get_info_app(app_name)

    if info_app:
        try:
            state = apps_state[app_name]
        except KeyError:
            apps_state[app_name] = state = AppsState.STARTED
        if state == AppsState.STARTS:
            return "Apps starts", 200
        url = info_app[1] + ":" + str(info_app[2])
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
        try:
            state = apps_state[app_name]
        except KeyError:
            apps_state[app_name] = state = AppsState.STARTED
        if state == AppsState.STARTS:
            return "Apps starts", 200
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
    try:
        app_name = data["appName"]
        server_key = data["serverKey"]
    except KeyError:
        abort(404)
    if server_key != get_server_key():
        abort (403)
    info_app = get_info_app(app_name)
    try:
        state = apps_state[app_name]
    except KeyError:
        apps_state[app_name] = state = AppsState.STARTED
    if state == AppsState.STARTS:
        return "OK", 208
    apps_state[app_name] = AppsState.STARTS
    if info_app is None:
        port, container_id = start_new_docker(app_name)
        set_info_app(app_name, url_host, port, container_id)
    else:
        port, container_id = restart_docker(app_name, info_app[3], info_app[2])
        update_info_app(app_name, url_host, port, container_id)
    apps_state[app_name] = AppsState.STARTED
    return "OK", 200
