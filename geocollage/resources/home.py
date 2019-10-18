from flask_restful import Resource
from flask import request
from ..data_service.db_service import fakeDB
from geocollage.services.decorators import only_superusers
from ..services import security


class HomeResource(Resource):
    def get(self):
        routes = {'posts': {'route': request.base_url + 'posts', 'methods': 'GET,POST'}}
        return routes
  