import json
from flask_restful import Resource
from flask import request
from flask import current_app as app
from geocollage.services import security
from geocollage.models.user import User
from geocollage import db
from geocollage.services.decorators import only_superusers, only_users, only_this_user
import stripe



class SessionsResource(Resource):
    @only_users
    def post(self, verified_token_payload):
        app.logger.info('POST sessions resource')
        user = security.get_user_by_uuid(verified_token_payload['id'])
        json_body = request.get_json()
        app.logger.debug(json_body)
        plan_id = json_body.get('plan_id')
        stripe.api_key = app.config['STRIPE_KEY']
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=user.id_stripe,
            subscription_data={
                'items': [{
                'plan': plan_id,
                }],
            },
            success_url='http://localhost:8080?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8080/account',
            )
        return {'status': 'OK', 'data': {'session_id': session.id}}, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

class WebhookResource(Resource):
    def post(self):
        app.logger.info('POST Webhook resource')
        payload = request.get_json()
        event = None
        stripe.api_key = app.config['STRIPE_KEY']

        try:
            event = stripe.Event.construct_from(
            payload, stripe.api_key
            )
        except ValueError as e:
            # Invalid payload
            return {}, 400

        # Handle the event
        app.logger.debug(f'The webhook endpoint detected the follwoing event: {event.type}')
        security.send_message('Admin', app.config['DEV_EMAIL'], f'The webhook endpoint detected the follwoing event: {event.type}')
        if event.type == 'customer.subscription.created':
            subscription = event.data.object # contains a stripe.PaymentIntent
            subscription = stripe.Subscription.modify(
                subscription.id,
                cancel_at_period_end=True
                )
        else:
            # Unexpected event type
            return {}, 400

        return {}, 200


        app.logger.debug(json_body)
        plan_id = json_body.get('plan_id')
        stripe.api_key = app.config['STRIPE_KEY']
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=user.id_stripe,
            subscription_data={
                'items': [{
                'plan': plan_id,
                }],
            },
            success_url='http://localhost:8080?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8080/account',
            )
        return {'status': 'OK', 'data': {'session_id': session.id}}, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}