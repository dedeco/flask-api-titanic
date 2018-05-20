
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'db','test.db')

DATABASE_URI = 'sqlite:///' + DATABASE
DEBUG = True
TRACK_MODIFICATIONS = False
