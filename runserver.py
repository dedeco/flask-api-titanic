import os

from config import DEBUG

from web.api.app import app
from web.api.models import *
from web.api.client import *

if __name__ == "__main__":
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port,debug=DEBUG)