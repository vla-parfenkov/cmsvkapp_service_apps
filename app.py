from flask import Flask, request
from flask_cors import CORS
from requests import get, post
import os

app = Flask(__name__)
CORS(app)

token = None

base = 'https://mobileapi.delivery-club.ru/m/1.59'
client_id_env = 'CLIENT_ID'
client_secret_env = 'CLIENT_SECRET'
client_auth_header = 'x-client-authorization'
access_control_origin = 'Access-Control-Allow-Origin'
content_type = 'Content-Type'

app.config['JSON_AS_ASCII'] = True


def get_token():
    res = get(os.path.join(base, 'client', 'token'), 
            params = {'client_id' : os.getenv(client_id_env), 'client_secret': os.getenv(client_secret_env)})
    print(res.headers)
    token = res.headers[client_auth_header]
    return token


@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    global token
    if token is None:
        token = get_token()
    if request.method == 'POST':
        response = post(url=(os.path.join(base, path)),
                   headers={client_auth_header: token, content_type: 'application/json'},
                   params = request.args, data = request.data)
    else:
        response = get(url=(os.path.join(base, path)),
                   headers={client_auth_header: token},
                   params = request.args)
    data = response.json()
    try:
        response_error = data["error"]
        response_status = data["status"]
        if response_error and response_status is not None:
            if responce_status == 401:
                token = get_token()
                if request.method == 'POST':
                    response = post(url=(os.path.join(base, path)),
                               headers={client_auth_header: token, content_type: 'application/json'},
                               params = request.args, data = request.data)
                else:
	            response = get(url=(os.path.join(base, path)),
                               headers={client_auth_header: token},
                               params = request.args)
    except KeyError:
        pass           
    response.headers[access_control_origin] = '*'
    return response.text, response.status_code


if __name__ == '__main__':
    app.run(threaded=True)
