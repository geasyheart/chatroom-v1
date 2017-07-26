from chatroom.ext import redis_init, socketio_init


def configure(app):
    redis_init.configure(app)
    socketio_init.configure(app)
