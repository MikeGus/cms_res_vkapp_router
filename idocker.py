import docker
from appconfig import app, get_port, lock





def start_new_docker(app_name):
    with app.app_context():
        client = docker.from_env()
        str_env = "APP_NAME=" + app_name
        port = get_port()
        container = client.containers.run('vktestapp', ports={'8080/tcp': port},
                    detach=True, environment=[str_env])
        return port, container.id

def restart_docker(app_name, container_id):
    with app.app_context():
        client = docker.from_env()
        try:
            container = client.containers.get(container_id)
            container.restart()
            return 0
        #if container remove, but exist in database
        except docker.errors.APIError:
            str_env = "APP_NAME=" + app_name
            port = get_port()
            container = client.containers.run('vktestapp', ports={'8080/tcp': port},
                        detach=True, environment=[str_env])
            return port, container.id