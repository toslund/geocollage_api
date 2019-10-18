print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! will import resources')
from geocollage.resources.home import HomeResource
from geocollage.resources.users import UsersResource, UserResource, User_meResource, UserPassword_Resource, UserSubscriptionResource
from geocollage.resources.private import Private
from geocollage.resources.auth import Auth, AuthReset
from geocollage.resources.posts import Posts
from geocollage.resources.plans import PlansResource
from geocollage.resources.stripebilling import SessionsResource, WebhookResource
from geocollage.resources.dump import DumpResource


print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! imported resources')

from geocollage import api

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! imported api')

api.add_resource(HomeResource, '/')

api.add_resource(Auth, '/auth')
api.add_resource(AuthReset, '/auth/reset')


api.add_resource(Private, '/private')

api.add_resource(DumpResource, '/dump/<dump_secret>')

api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<user_id>')
api.add_resource(UserPassword_Resource, '/users/<user_id>/password')
api.add_resource(UserSubscriptionResource, '/users/<user_id>/subscription')
api.add_resource(User_meResource, '/users/me')

api.add_resource(Posts, '/posts')

api.add_resource(PlansResource, '/plans')
api.add_resource(SessionsResource, '/session')
api.add_resource(WebhookResource, '/webhook/endpoint')


print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! added resources')

from geocollage.models.post import Post
from geocollage.models.user import User

# from geocollage.data_service.real_database import session, init_db, teardown_session
# from geocollage.data_service.models import User


# app = Flask(__name__)
# # app.config.from_object('geocollage.default_settings')
# app.config.from_pyfile('dev.cfg')
# api = Api(app)

# db = SQLAlchemy(app)

