from flask_restful import Resource
from flask import request
from flask import current_app as app
from geocollage.services import security
from geocollage.models.user import User
from geocollage import db
from geocollage.services.decorators import only_superusers, only_users, only_this_user
import stripe


class UsersResource(Resource):
    @only_superusers
    def get(self, verified_token_payload):
        app.logger.info('GET users resource')
        users = User.query.all()
        return {'users': [user.dump() for user in users]}, 200, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        app.logger.info('POST user resource')
        app.logger.debug(request)
        json_body = request.get_json()
        app.logger.debug(json_body)
        username = json_body.get('username')
        app.logger.debug(f'username: {username}')
        password = json_body.get('password')
        app.logger.debug(f'password: {password}')
        confirm_password = json_body.get('confirm_password')
        app.logger.debug(f'confirm_password: {confirm_password}')
        email = json_body.get('email')
        app.logger.debug(f'email: {email}')
        invite_code = json_body.get('invite_code')
        app.logger.debug(f'invite code: {invite_code}')
        favorite_color = json_body.get('favorite_color', 'I hate colors')
        app.logger.debug(f'favorite_color code: {favorite_color}')

        if app.config['REQUIRE_INVITE'] == 'true':
            if not invite_code or invite_code != app.config['INVITE_CODE']:
                return {'error': 'Invalid invite code'}, 400, {'Access-Control-Allow-Origin': '*'}
        if password and email and favorite_color.lower() in ['red', 'blue', 'yellow']:
            password_error = security.passwordErrors(password, confirm_password)
            if password_error:
                return {'error': 'password error', 'message': password_error}, 400, {'Access-Control-Allow-Origin': '*'}
            if username:
                user = User.query.filter_by(username=username).first()
                if user:
                    return {'error': 'username error'}, 400, {'Access-Control-Allow-Origin': '*'}
            user = User.query.filter_by(email=email).first()
            if user:
                return {'error': 'email already taken', 'message': 'Please choose a different email. If you already have an account, please sign in.'}, 400, {'Access-Control-Allow-Origin': '*'}
            user = User(username=username, password=security.hash_password(password), email=email)
            db.session.add(user)
            stripe.api_key = app.config['STRIPE_KEY']
            customer = stripe.Customer.create(
                email=user.email	
                )
            user.id_stripe = customer.id    
            db.session.commit()

            ## The following section attempts to give new users a free trial subscription if the app is in alpha phase, there is a plan_id stored, and a valid coupon for 100% off
            if app.config.get('RELEASE') == 'alpha' and app.config.get('PLAN_ID'):
                coupon_id = None
                coupons = stripe.Coupon.list()
                for coupon in coupons:
                    if coupon.percent_off == 100:
                        coupon_id = coupon.id
                        break
                if coupon_id:    
                    subscription = stripe.Subscription.create(
                        customer=customer.id ,
                        items=[{'plan': app.config.get('PLAN_ID')}],
                        coupon=coupon_id,
                    )

            token = security.generate_token(email)
            user_dict = user.to_dict()
            user_dict['token'] = token
            security.send_welcome_message(user.email)
            return user_dict, 200, {'Access-Control-Allow-Origin': '*'}
        return {'error': 'some'}, 400, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET,POST'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,POST',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

class UserResource(Resource):
    @only_this_user
    def get(self, user_id, verified_token_payload):
        user = security.get_user_by_uuid(verified_token_payload['id'])
        if user:
            return user.to_dict(), 200, {'Access-Control-Allow-Origin': '*'}
        else: #Should only happen if token is verified but user has been deleted
            return None    

    def delete(self, user_id):
        #Get token
        app.logger.debug(f'Delete users/{user_id}/password')
        app.logger.debug(f'Authorization: {request.authorization}')
        email = request.authorization.get('username')
        password = request.authorization.get('password')
        if not security.verify_basic_auth(email, password):
            return {'error': 'invalid credentials'}, 401, {'Access-Control-Allow-Origin': '*'}
        user = security.get_user_by_email(email)
        if user_id != user.id_uuid:
            app.logger.debug(f'user.id_uuid: {user.id_uuid} does not match uuid from request: {user_id}')
            return {'error': 'invalid username or password', 'message': 'Invalid credentials'}, 401, \
                {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
        db.session.delete(user)
        db.session.commit()
        return{'status': 'OK'}, 200, {'Access-Control-Allow-Origin': '*'}

    # @only_this_user
    # def patch(self, user_id):
    #     password = request.get_json().get('password')
    #     data = security.verify_token(token)
    #     if user_id != data.get('id'):
    #         return {'error': 'forbidden'}, {'Access-Control-Allow-Origin': '*'}
    
    def options(self, user_id):
        return {'Allow': 'GET,DELETE,PATCH'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,POST,DELETE,PATCH',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

class UserSubscriptionResource(Resource):
    @only_this_user
    def get(self, user_id, verified_token_payload):
        try:
            user = security.get_user_by_uuid(verified_token_payload['id'])
            stripe.api_key = app.config['STRIPE_KEY']
            customer = stripe.Customer.retrieve(user.id_stripe)
            subscription = list(customer.subscriptions)[0]
            product = stripe.Product.retrieve(subscription['plan']['product'])
        except IndexError as e:
            app.logger.debug(f'Error retrieving customer subscription: {e}')
            subscription = None    
            product = None
        except Exception as e:
            app.logger.debug(f'Error retrieving customer subscription: {e}')
            return {'error': {'status': 'error while retrieving customer subscription', 'message': 'There was an error while retrieving your subscription. Please try refreshing your page or contacting support.'}}, 500, \
                {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}  
        return {'status': 'OK', 'data': {'subscription': subscription, 'product': product}}, 200, {'Access-Control-Allow-Origin': '*'} 

    # def delete(self, user_id):
    #     #Get token
    #     app.logger.debug(f'Delete users/{user_id}/password')
    #     app.logger.debug(f'Authorization: {request.authorization}')
    #     email = request.authorization.get('username')
    #     password = request.authorization.get('password')
    #     if not security.verify_basic_auth(email, password):
    #         return {'error': 'invalid credentials'}, 401, {'Access-Control-Allow-Origin': '*'}
    #     user = security.get_user_by_email(email)
    #     if user_id != user.id_uuid:
    #         app.logger.debug(f'user.id_uuid: {user.id_uuid} does not match uuid from request: {user_id}')
    #         return {'error': 'invalid username or password', 'message': 'Invalid credentials'}, 401, \
    #             {'Access-Control-Allow-Origin': '*',
    #                 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
    #     db.session.delete(user)
    #     db.session.commit()
    #     return{'status': 'OK'}, 200, {'Access-Control-Allow-Origin': '*'}

    # @only_this_user
    # def patch(self, user_id):
    #     password = request.get_json().get('password')
    #     data = security.verify_token(token)
    #     if user_id != data.get('id'):
    #         return {'error': 'forbidden'}, {'Access-Control-Allow-Origin': '*'}
    
    def options(self, user_id):
        return {'Allow': 'GET,DELETE,PATCH'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}                


class UserPassword_Resource(Resource):
    def put(self, user_id):
        app.logger.debug(f'Put users/{user_id}/password')
        app.logger.debug(f'Authorization: {request.authorization}')
        email = request.authorization.get('username')
        password = request.authorization.get('password')
        if not security.verify_basic_auth(email, password):
            return {'error': 'invalid credentials'}, 401, {'Access-Control-Allow-Origin': '*'}
        user = security.get_user_by_email(email)
        if user_id != user.id_uuid:
            app.logger.debug(f'user.id_uuid: {user.id_uuid} does not match uuid from request: {user_id}')
            return {'error': 'invalid username or password', 'message': 'Invalid credentials'}, 401, \
                {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}
        new_password = request.get_json().get('password')
        confirm_new_password = request.get_json().get('confirm_password')
        password_error = security.passwordErrors(new_password, confirm_new_password)
        if password_error:
            return {'error': 'password error', 'message': password_error}, 400, \
                {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

        user.password = security.hash_password(new_password)
        db.session.commit()
        return {'satus': 'OK', 'message': 'Your password has been succesfully set'}, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self, user_id):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'}

class User_meResource(Resource):
    def get(self):
        token = request.args.get('token')
        if not token:
            return {'error': 'invalid credentials'}, {'Access-Control-Allow-Origin': '*'}
        data = security.verify_token(token)
        if not data:
            return {'error': 'invalid credentials'}, {'Access-Control-Allow-Origin': '*'}
        user_id = data['id']
        user = User.query.filter_by(id_uuid=user_id).first()
        return user.to_dict(), {'Access-Control-Allow-Origin': '*'}


