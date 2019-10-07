from datetime import datetime, timedelta
from orm import *

db.drop_all()
db.create_all()


def create_data():
    for i in range(10):
        db.session.add(Device(name='d%s' % i, longitude=121 +
                              (i/100), latitude=23 + (i/100)))
        for j in range(10):
            db.session.add(DhtLog(timestamp=datetime.utcnow() + timedelta(minutes=j), temperature=23 +
                                (j/100), humidity=80 + (j/100), device_id=i))
    db.session.commit()

create_data()