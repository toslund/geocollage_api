import sys
from geocollage import db
from geocollage.models.user import User
from geocollage.services import security

"""Expects sys args: EMAIL PASSWORD"""

# count the arguments
arguments = len(sys.argv) - 1
if arguments != 2:
    raise Exception('Invalid number of arguments')

email = sys.argv[1]
password = sys.argv[2]

if "@" not in email:
    raise Exception('Invalid email')

user = User(email=email, password=security.hash_password(password), role="superuser")
db.session.add(user)
db.session.commit()


