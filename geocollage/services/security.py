import time, os, re
from passlib.hash import pbkdf2_sha256
from ..data_service import db_service
import jwt
import requests
from flask import current_app as app
from geocollage.models.user import User

secret = 'super_duper_secret'

def is_superuser(token):
    user = verified_user(token)
    try:
        return user.role == 'superuser'
    except AttributeError:
        return False

def get_superuser(token):
    user = verified_user(token)
    try:
        if user.role == 'superuser':
            return user
        else:
            return None    
    except AttributeError:
        return None

def is_user(token):
    user = verified_user(token)
    if user:
        return True
    return False

def generate_token(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    current_time = time.time()
    # #add 30 minutes
    # expiration_time = current_time + 1800
    # add 24 hours
    expiration_time = current_time + 86400
    token = jwt.encode({'exp': expiration_time, 'email': email, 'role': user.role, 'id': user.id_uuid}, app.config['SECRET'], algorithm='HS256').decode('utf-8')
    return token

def generate_reset_token(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    current_time = time.time()
    # #add 30 minutes
    # expiration_time = current_time + 1800
    # add 1 hour
    expiration_time = current_time + 3600
    token = jwt.encode({'exp': expiration_time, 'email': email, 'role': user.role, 'id': user.id_uuid}, app.config['SECRET'], algorithm='HS256').decode('utf-8')
    return token

def send_message(name, email, message):
    if os.environ.get("ENV") == 'prod':
        pass
    else:
        email = app.config['DEV_EMAIL']
    return requests.post(
        f'https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages',
        auth=("api", app.config['MAILGUN_KEY']),
        data={"from": f"Mailgun Sandbox <postmaster@{app.config['MAILGUN_DOMAIN']}.mailgun.org>",
            "to": f"{name} <{email}>",
            "subject": f"Hello {name}",
            "text": message})

def send_welcome_message(email):
    if os.environ.get("ENV") == 'prod':
        pass
    else:
        email = app.config['DEV_EMAIL']
    return requests.post(
        f'https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages',
        auth=("api", app.config['MAILGUN_KEY']),
        data={"from": f"Mailgun Sandbox <postmaster@{app.config['MAILGUN_DOMAIN']}.mailgun.org>",
            "to": f"Timothy Oslund <{email}>",
            "subject": "Hello Timothy Oslund",
            "text": f"Hi, Thanks for creating an account with Collage Maker. No further action is needed."})

def send_reset_message(email, token):
    reset_url = app.config['FRONT_END_BASE_URL'] + f'auth/reset?token={token}'
    if os.environ.get("ENV") == 'prod':
        pass
    else:
        email = app.config['DEV_EMAIL']
    return requests.post(
        f'https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages',
        auth=("api", app.config['MAILGUN_KEY']),
        data={"from": f"Mailgun Sandbox <postmaster@{app.config['MAILGUN_DOMAIN']}.mailgun.org>",
            "to": f"Timothy Oslund <{email}>",
            "subject": "Hello Timothy Oslund",
            "text": f"Hi, Thanks It looks like you have requested to reset your password. The following link will be valid for the next 24 hours: {reset_url}"})               

def verified_token(token):
    app.logger.debug(f'verifying token: {token}')
    try:
        verifed_token = jwt.decode(token.encode('utf-8'), app.config['SECRET'])
        app.logger.debug(f'verified token: {verifed_token}')
        return verifed_token
    except jwt.InvalidTokenError as e:
        app.logger.debug(f'error validating token: {e}')
        return None  # do something sensible here, e.g. return HTTP 403 status code

def get_user_by_uuid(id_uuid):
    user = User.query.filter_by(id_uuid=id_uuid).first()
    return user

def get_user_by_email(email):
    app.logger.debug(f'getting user by email: {email}')
    user = User.query.filter_by(email=email).first()
    app.logger.debug(user)
    return user


def verified_user(token):
    app.logger.debug('Checking to see if user is verified with token')
    secret = app.config['SECRET']
    app.logger.debug(f'token: {token}')
    app.logger.debug(f'secret: {secret}')

    if not token:
        app.logger.debug('No token was provided')
        return None
    try:
        payload = jwt.decode(token.encode('utf-8'), secret)
        app.logger.debug(f'payload: {payload}')
    except jwt.InvalidTokenError as e:
        app.logger.warning('Invalid token error')
        app.logger.warning(e)
        return None
    user = User.query.filter_by(email=payload['email']).first()
    if not user:
        app.logger.debug('No user found in DB')
        return None
    return user

def passwordErrors(password, password2):
    if password != password2:
        return 'Passwords do not match'
    if len(password) < 6 or len(password) > 16:
        return 'Password must be between 6 and 16 characters'
    has_symbol = False    
    for n in password:
        if n in """ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""":
            has_symbol = True
            break
    if not has_symbol:
        return 'Password must contain 1 special character'
    has_number = False    
    for n in password:
        if n in "1234567890":
            has_number = True
            break
    if not has_number:
        return 'Password must contain 1 number'    
    return None

def hash_password(password):
    hash = pbkdf2_sha256.hash(password)
    return hash

def verify_basic_auth(email, password):
    try:
        app.logger.debug(f'Verifying basic auth for user: {email} and password: {password}******')
        user = User.query.filter_by(email=email).first()
        verified_password = pbkdf2_sha256.verify(password, user.password)
        app.logger.debug(f'Verified password: {verified_password}')
        return verified_password
    except Exception as e:
        app.logger.debug(f'Error verifying basic auth: {e}')
