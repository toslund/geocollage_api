from flask_restful import Resource
from flask import current_app as app
from flask import request
from ..data_service.db_service import fakeDB
from geocollage import db
from geocollage.models.post import Post
from geocollage.models.user import User


class Posts(Resource):
    def get(self):
        app.logger.info('GET posts')
        posts = Post.query.all()
        return [post.to_dict() for post in posts]
    def post(self):
        # print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        # print(request)
        title = request.get_json().get('title')
        content = request.get_json().get('content')
        user_id = request.get_json().get('user_id')
        if not title or not content or not user_id:
            return {'error': 'missing required data'}
        verified_user = User.query.get(user_id)
        if not verified_user:
            return {'error': 'invalid user'}
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post.to_dict()
