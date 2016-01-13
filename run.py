__author__ = 'FRAMGIA\nguyen.huy.quyet'

from flask_demo import app, db

if __name__ == '__main__':
    app.debug = True
    db.create_all(app=app)
    app.run()
