import uuid, calendar
from datetime import datetime
from geocollage import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda:str(uuid.uuid4()))
    title = db.Column(db.String(20), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id_uuid'), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.date_posted}'"

    def to_dict(self):
        return {
    'id_uuid': self.id_uuid,
    'title': self.title,
    'date_created': calendar.timegm(self.date_created.timetuple()) * 1000,
    'publish_date': calendar.timegm(self.publish_date.timetuple()) * 1000,
    'content': self.content,
    'user_id': self.user_id}

    def dump(self):
        return {
    'id': self.id,
    'id_uuid': self.id_uuid,
    'title': self.title,
    'date_created': calendar.timegm(self.date_created.timetuple()) * 1000,
    'publish_date': calendar.timegm(self.publish_date.timetuple()) * 1000,
    'content': self.content,
    'user_id': self.user_id}
