import uuid
from werkzeug.security import generate_password_hash

from web.api.app import app
from web.api.models import *

def populate():
    u = User()
    u.id = 1
    u.public_id = str(uuid.uuid4())
    u.name = 'dedeco'
    u.password = generate_password_hash('dragon', method='sha256')
    u.admin = True
    
    db.session.add(u)

    db.session.commit()

with app.test_request_context():
    db.drop_all() 
    db.create_all()
    populate()