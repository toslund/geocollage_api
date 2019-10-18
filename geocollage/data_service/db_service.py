import json, os
from uuid import uuid4
from geocollage.services import security

json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'users.json')
class fakeDB:
    pass

    @staticmethod
    def users():
        with open(json_file, 'r') as read_file:
            data = json.load(read_file)
            return data

    @staticmethod
    def create_user(username, password):
        with open(json_file, 'r') as read_file:     
            data = json.load(read_file)
        for key, user in data.items():
            if user['username'] == username:
                return None
        id = str(uuid4())
        data[id]= {"username": username, "pw_hash": security.hash_password(password)}
        with open('db/users.json', 'w') as write_file:     
            json.dump(data, write_file)
            return data[id]
        return None    

