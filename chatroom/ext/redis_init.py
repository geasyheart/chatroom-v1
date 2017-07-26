from flask_redis import FlaskRedis

redis_db = FlaskRedis()


def configure(app):
    redis_db.init_app(app)
