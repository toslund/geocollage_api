from flask_restful import Resource
from flask import request
from ..data_service.db_service import fakeDB
from geocollage.services.decorators import only_superusers
from ..services import security

private_data = {'data': 'super private stuff'}

class Private(Resource):
    @only_superusers
    def get(self, verified_token_payload):
        user = security.get_user_by_uuid(verified_token_payload['id'])
        data = private_data
        data['user'] = user.id
        return data
    def post(self):
        return {'error': 'wrong verb'}   