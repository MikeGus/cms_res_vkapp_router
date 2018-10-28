import docker
from appconfig import app, get_port, lock, get_server_key





def start_new_docker(app_name):
    with app.app_context():
        client = docker.from_env()
        str_env = "APP_NAME=" + app_name
        server_key_env = "SERVER_KEY=" + get_server_key()
        port = get_port()
        container = client.containers.run('vktestapp', ports={'8080/tcp': port},
                    detach=True, environment=[str_env, server_key_env])
        return port, container.id

def restart_docker(app_name, container_id, port):
    with app.app_context():
        client = docker.from_env()
        try:
            container = client.containers.get(container_id)
            container.stop()
            container.remove()
        #if container remove, but exist in database
        except docker.errors.APIError:
            port = get_port()
        str_env = "APP_NAME=" + app_name
        server_key_env = "SERVER_KEY=" + get_server_key()
        container = client.containers.run('vktestapp', ports={'8080/tcp': port},
                    detach=True, environment=[str_env, server_key_env])
        return port, container.id