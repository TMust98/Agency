import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_very_very_very_very_very_longest_SECRET_KEY'
