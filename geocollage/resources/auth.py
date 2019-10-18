from ..services import security
from flask import request
from flask_restful import Resource
from geocollage import db


class Auth(Resource):
    def post(self):
        print('%%%%%%%%%%%%% AUTH')
        print(request.authorization)
        email = request.authorization.get('username')
        password = request.authorization.get('password')
        print(email, password)
        if security.verify_basic_auth(email, password):
            return {'token': security.generate_token(email)}, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
        else:
            return {'error': 'invalid username or password'}, 401, \
                   {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

    def get(self):
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # username = request.args.get('username')
        # password = request.args.get('password')
        # print(username, password)
        # if verify_user(username, password):
        #     return {'token': genearte_token(username)}
        return {'error': 'invalid verb'}

    def options(self):
        return {'Allow': 'POST'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

class AuthReset(Resource):
    def post(self):
        #Get token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            return {'error': 'invalid credentials'}, 401, {'Access-Control-Allow-Origin': '*'}
        user = security.verified_user(token)
        if not user:
            return {'error': 'invalid username or password'}, 401, \
                {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
        password = request.get_json().get('password')
        confirm_password = request.get_json().get('confirm_password')
        password_error = security.passwordErrors(password, confirm_password)
        if password_error:
            return {'error': 'password error', 'message': password_error}, 400, \
                {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

        if user and not password_error:
            user.password = security.hash_password(password)
            db.session.commit()
            return {'token': security.generate_token(user.email), 'message': 'Your password has been succesfully updated and you are logged in.'}, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
       

    def get(self):
        email = request.args.get('email')
        token = security.generate_reset_token(email)
        if token:
            security.send_reset_message(email, token)
            return {'message': 'If this email was associated with an account, we will send further instructions'}, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # username = request.args.get('username')
        # password = request.args.get('password')
        # print(username, password)
        # if verify_user(username, password):
        #     return {'token': genearte_token(username)}
        return {'message': 'If this email was associated with an account, we will send further instructions.'}, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

    def options(self):
        return {'Allow': 'POST'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': ['POST', 'GET'],
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

