from web.api.app import app
from web.api.models import *

def save(df):

    passengers = []

    records = df.to_dict('records')

    for row in records:
        p = Passenger(row)
        passengers.append(p)

    for p in passengers:
        db.session.add(p)

    db.session.commit()

from ml.models import train, restore

with app.test_request_context():
    print ('Trainning model. It will take a while... (~ 5 minutos)')
    train.run()
    print ('Saving model...')
    save(restore.run())
    print ('Saved!')