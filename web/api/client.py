import json
import jwt
import datetime

from flask import Flask, request, make_response
from functools import wraps
from werkzeug.security import check_password_hash

from .utils import json_response, JSON_MIME_TYPE, escape

from .models import db, User, Passenger
from .app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return json_response(json.dumps({'error' : 'Token is missing.'})), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.session.query(User).filter_by(public_id=data['public_id']).first()
        except:
            return json_response(json.dumps({'error' : 'Token is not valid.'})), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/ping', methods=['GET','POST'])
@token_required
def ping():
    return json_response(json.dumps({"ping":"pong"}))

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required."'})

    user = db.session.query(User).filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required."'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return json_response(json.dumps({'token' : token.decode('UTF-8')}))

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required."'})

@app.route('/survivals/<name>', methods=['GET','POST'])
@app.route('/survivals', methods=['POST'])
def get_survivals(name=None):

    if request.method == 'POST':

        if request.content_type != JSON_MIME_TYPE:
            error = json.dumps({'error': 'Invalid Content Type'})
            return json_response(error, 400)

        data = request.json

        if not data.get('name'):
            error = json.dumps({'error': 'Missing field/s (name)'})
            return json_response(error, 400)

        if  not len(data.get('name')) > 3:
            error = json.dumps({'error': 'Name must be at least 3 characters'})
            return json_response(error, 400)

        name = escape(data.get('name')) 

    else:
        name =  escape(name)

    q = db.session.query(Passenger)\
        .filter(Passenger.Name.ilike('%' + name + '%'))

    pgers = [ x.dict() for x in q.all()]

    response = {}
    response['Passengers'] = pgers

    return json_response(json.dumps(response))