from flask import request
from functools import wraps
from geocollage.services import security
from flask import current_app as app


def allow_cors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs), {'Access-Control-Allow-Origin': '*'}
    return decorated_function

def only_users(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # token = request.args.get('token')
        # verified_token_payload = security.verified_token(token)
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = None
        verified_token_payload = security.verified_token(token)
        if not verified_token_payload:
            return {'error': 'invalid credentials', 'message': 'Invalid credentials aka You aint a superuser'}
        return f(*args, **kwargs, verified_token_payload=verified_token_payload)
    return decorated_function    

def only_this_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = None
        verified_token_payload = security.verified_token(token)
        try:
            app.logger.debug(f'token id: {verified_token_payload["id"]}')
            app.logger.debug(f'request id: {kwargs["user_id"]}')
        except:
            pass
        if not verified_token_payload or kwargs['user_id'] != verified_token_payload['id']:
            return {'error': 'invalid credentials', 'message': 'Invalid credentials aka you aint this user'}
        return f(*args, **kwargs, verified_token_payload=verified_token_payload)
    return decorated_function    

def only_superusers(f):
    ''' Only allows requests buy superusers without querying the db. Adds verified token as kwarg'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #Get token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = None
        verified_token_payload = security.verified_token(token)
        if not verified_token_payload or not verified_token_payload['role'] == 'superuser':
            return {'error': 'invalid credentials', 'message': 'Invalid credentials aka You aint a superuser'}
        return f(*args, **kwargs, verified_token_payload=verified_token_payload)
    return decorated_function    
