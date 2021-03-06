import os

from flask import Flask

from chatroom import ext
from chatroom import settings
from chatroom.ext.socketio_init import socketio
from chatroom.modules.urls import module, register_socketio_url
from chatroom.ext.redis_init import redis_db


def create_app(api_server=False):
    app = Flask("chat", template_folder="chatroom/templates")
    app.config.from_object(settings)
    if 'CHAT_CONF' in os.environ:
        app.config.from_envvar('CHAT_CONF')
    ext.configure(app)
    if not api_server:
        register_socketio_url()
    app.register_blueprint(module)
    # 删除所有的key
    for key in redis_db.keys("chat:*"):
        redis_db.delete(key)
    return app
