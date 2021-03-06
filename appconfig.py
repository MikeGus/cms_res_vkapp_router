import sqlite3
import threading
import socket
from flask import _app_ctx_stack, Flask
from enum import Enum

app = Flask(__name__)

class AppsState(Enum):
    STOPPED = 1
    STARTED = 2
    STARTS = 3

DATABASE = 'Database/Apps.db'

url_host = "http://localhost"
start_port = 4000

server_key_global = None
apps_state = {}

lock = threading.Lock()

def get_db():
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is None:
        db = _app_ctx_stack.top._database = sqlite3.connect(DATABASE)
    return db

def get_server_key():
    global server_key_global
    if server_key_global is None:
        f = open('server_key', 'r')
        server_key_global = f.read()
        server_key_global = server_key_global[0:-1]
        f.close()
    return server_key_global


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is not None:
        db.close()


def get_port():
    port = getattr(_app_ctx_stack.top, '_lastport', None)
    if port is None:
        port = _app_ctx_stack.top._lastport = get_last_port_for_url(url_host)
    if  port is None:
        port = _app_ctx_stack.top._lastport = start_port
    else:
        _app_ctx_stack.top._lastport = port + 1
        return port + 1 
    return port

def get_last_port_for_url(url):
    with app.app_context():
        cursor = get_db().cursor()
        sql = "SELECT port FROM Apps WHERE url = ? ORDER BY port DESC LIMIT 1"
        cursor.execute(sql, [url])
        res = cursor.fetchone()
        if res is None:
            return None
        else:
            return res[0]

def check_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', port))
        sock.listen(5)
        sock.close()
    except socket.error as e:
        return False
    return True
