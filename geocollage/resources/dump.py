from flask_restful import Resource
from flask import request
from flask import current_app as app
from geocollage.services import security
from geocollage.models.user import User
from geocollage.models.post import Post
from geocollage import db

class DumpResource(Resource):
    def get(self, dump_secret):
        if app.config['DUMP_SECRET'] != dump_secret:
            return {'error': 'invalid credentials'}, 400, {'Access-Control-Allow-Origin': '*'}
        token = request.args.get('token')
        if not security.is_superuser(token):
            return {'error': 'invalid credentials'}, 400, {'Access-Control-Allow-Origin': '*'}

        users = User.query.all()
        users_dicts = [user.dump() for user in users]

        posts = Post.query.all()
        posts_dicts = [post.dump() for post in posts]



        return {'users': users_dicts,
                'posts': posts_dicts}, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept'}








