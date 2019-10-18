import uuid
from geocollage import db
# from my_api.models import Post

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_uuid = db.Column(db.String(36), unique=True, default=lambda:str(uuid.uuid4()))
    id_stripe = db.Column(db.String(255))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), unique=False, nullable=False, default='unverified_user')
    image_file = db.Column(db.String(36), nullable=False, default='default.jpg')
    password = db.Column(db.String(87), nullable = False)
    posts = db.relationship('Post', cascade="all,delete", backref='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def to_dict(self):
        return {
    'id': self.id_uuid,
    'username': self.username,
    'email': self.email,
    'role': self.role,
    'image_file': self.image_file}

    def dump(self):
        return {
    'id': self.id,
    'id_uuid': self.id_uuid,
    'id_stripe': self.id_stripe,
    'username': self.username,
    'email': self.email,
    'role': self.role,
    'image_file': self.image_file,
    'posts': [post.id for post in self.posts]}
