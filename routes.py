from flask import Flask

app = Flask(__name__)


@app.route('/')
def put_app(app_name):
    #put app in base
    return app_name, 200


@app.route('/<app_name>')
def proxy(app_name):
    #get app from base
    return app_name