import docker
from appconfig import app, get_port, lock





def start_new_docker(appName):
    with app.app_context():
        client = docker.from_env()
        str_env = "APP_Name=" + appName
        port = get_port()
        container = client.containers.run('vktestapp', ports={'8080/tcp': port},
                    detach=True, environment=[str_env])
        return port, container.id

def restart_docker(appName, containerId):
    with app.app_context():
        client = docker.from_env()
        try:
            container = client.containers.get(containerId)
            container.restart()
            return 0
        #if container remove, but exist in database
        except Exception:
            str_env = "APP_Name=" + appName
            port = get_port()
            container = client.containers.run('vktestapp', ports={'8080/tcp': port},
                        detach=True, environment=[str_env])
            return port, container.id