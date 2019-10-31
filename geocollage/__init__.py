import os, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api


print('Will create app')
print('__name__ =' + __name__)
app = Flask(__name__)
print(app)
# app.config.from_object('geocollage.default_settings')
if os.environ.get("ENV") == "dev":
    print('App running in dev mode. YOU SHOULD NOT SEE THIS IN PRODUCTION.')
    app.config.from_pyfile('dev.cfg')
else: 
    print('App running in production mode.')
    app.config.from_pyfile('prod.cfg')

# configure logging
if os.environ.get("LOGGING"):
    logging.basicConfig(level=os.environ.get("LOGGING"))
else:   
    logging.basicConfig(level=logging.DEBUG)

api = Api(app)

#change name of databse url env from the heroku/config default to what flask-sqlalchemy expcets. This prevents you from having to manaully if deploying to heroku.
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
app.logger.debug(f'The sql alchemy database url is: {app.config["SQLALCHEMY_DATABASE_URI"]}')
db = SQLAlchemy(app)

print('Will import program')
from geocollage import program

print('Finished importing program')
