# Intro  
geocollage is a basic backend API for GeoCollage It uses Stripe for managing billing, customers, and products and uses Mailgun for email services.
# Getting Started
## Running in Dev

Install requirments:  
`pip install -e .`  
  
Rename dev.cfg.example to dev.cfg and fill in required vars.  
  
Set ENV vars:  
`export FLASK_APP=geocollage`  
`export ENV=dev`  
  
Create tables:  
`python manage.py`  
  
Create super user:  
`python create_superuser.py SuperUser superuser@example.com password`  
  
Optionally, set logging preference. Defaults to INFO in dev mode:  
`export LOGGING=DEBUG`  
  
Serve with flask:  
`flask run`  

## Running in Production
*with heroku*

Rename prod.cfg.example to prod.cfg  

Create a Heroku project:  
`heroku create`  
  
Provision a database:  
`heroku addons:create heroku-postgresql:hobby-dev`  
  
Set required env vars:  
`heroku config:set SECRET=My_aPp_sEcReT`  
`heroku config:set SECRET_KEY=ASDFASDFASDFASDFASDASDF`  
`heroku config:set DUMP_SECRET=super_secret_dump_secret`      
`heroku config:set MAILGUN_KEY=123123123123123123123123123`  
`heroku config:set STRIPE_KEY=321321321321321321321321321`  
`heroku config:set DEV_EMAIL=example@example.com`  
`heroku config:set STRIPE_KEY=321321321321321321321321321`  
`heroku config:set FRONT_END_BASE_URL=https://www.my-amazing-site-example.com/`  

Set optional env vars:
`heroku config:set INVITE_CODE=invite2019`  
`heroku config:set REQUIRE_INVITE=yes`  

Explicitly set ENV to prod:
`heroku config:set ENV=prod`  
    
Push to heroku:  
`git push heroku master` 

Fill in db with tables:    
`heroku run python manage.py`

Create super user:  
`heroku run python create_superuser.py SuperUser superuser@example.com password`
  

# Routes

## /posts
### GET
### POST

## /users
### GET
### POST

## /users/:id
### GET
### POST

## /users/:id/password
### PATCH

## /users/:id/subscription
### GET

