from flask_restful import Resource
from flask import request
from flask import current_app as app
from geocollage.services import security
from geocollage.models.user import User
from geocollage import db
from geocollage.services.decorators import only_superusers, only_users, only_this_user
import stripe



class PlansResource(Resource):
    def get(self):
        app.logger.info('GET plans resource')
        stripe.api_key = app.config['STRIPE_KEY']
        plans = stripe.Plan.list()
        return {'plans': [plan for plan in plans if plan['active']]}, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}