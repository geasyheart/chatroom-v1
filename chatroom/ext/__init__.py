from chatroom.ext import redis_init, socketio_init, error_handler


def configure(app):
    error_handler.configure(app)
    redis_init.configure(app)
    socketio_init.configure(app)
