import os,json
from datetime import datetime
from geocollage import db
from geocollage.services import security
from geocollage.models.user import User
from geocollage.models.post import Post

#              ]

with open('data.json', 'r') as f:
    data = json.load(f)


# date_format = '2019-03-13'

# try:
#     fake_password = os.environ['FAKE_PASSWORD']
# except:
#     fake_password = 'password'

users = {}
posts = []

for post in data['posts']:
    new_post = Post(
                title = post['title'],
                content = post['content'],
                user_id = post['user_id'])
    db.session.add(new_post)
    posts.append(new_post)

for user in data['users']:
    new_user = User(id=user['id'],
                 username=user['username'],
                 email=user['email'],
                 image_file=user['image_file'],
                 posts=[post for post in posts if post.user_id == user['id']],
                 password=user['password'])
    db.session.add(new_user)
    users[new_user.id] = new_user




db.session.commit()


