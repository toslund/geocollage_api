from setuptools import setup

setup(
    name='geocollage',
    packages=['geocollage'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        'passlib',
        'SQLAlchemy',
        'Flask-SQLAlchemy',
        'PyJWT',
        'gunicorn',
        'psycopg2',
        'python-slugify',
        'bleach',
        'boto3',
        'stripe'
    ],
)
