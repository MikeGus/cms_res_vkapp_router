from requests import head, get, exceptions
from appconfig import app, url_host, get_server_key
from idocker import start_new_docker, restart_docker, remove_docker
from Database.dbquery import get_info_app, update_info_app, get_all_apps, delete_app
from time import sleep

error_counter = 3
restart_counter = 3
url_back = "https://cmsvkappback.site/api/apps/"
#app_name : [error_counter, restart_counter, port, conteiner]
problem_apps = {}
        

def main_lopp():
    with app.app_context():
        while True:
            apps = get_all_apps()
            find_problem_apps(apps)
            try_deploy_problem_apps()
            sleep(60)


def find_problem_apps(apps):
    for info_app in apps:
        url = info_app[1] + ":" + str(info_app[2])
        try:
            response = head(url)
            if response.status_code == 500:
                try:
                    #incriment error
                    problem_apps[info_app[0]][0] += 1 
                except KeyError:
                    problem_apps[info_app[0]] = [1, 0, info_app[2], info_app[3]]
            else:
                problem_apps.pop(info_app[0], None)
        except exceptions.ConnectionError:
            try:
                #incriment error
                problem_apps[info_app[0]][0] += 1 
            except KeyError:
                problem_apps[info_app[0]] = [1, 0, info_app[2], info_app[3]]

def try_deploy_problem_apps():
    for key, value in problem_apps.iteritems():
        if value[1] == restart_counter:
            remove_docker(value[3])
            delete_app(key)
            value[0] = 0
            url =  url_back + '/' + key + '/stop'
            payload = {'server_key': get_server_key()}
            response = get(url, params=payload)
            problem_apps.pop(key, None)
            #send push to client
        if value[0] == error_counter:
            port, container_id = restart_docker(key, value[3], value[2])
            update_info_app(app_name, url_host, port, container_id)
            value[1] += 1
            value[0] = 0


main_lopp()


