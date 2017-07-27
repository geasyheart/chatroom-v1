from flask import Blueprint

from chatroom.ext.socketio_init import socketio
from chatroom.modules.events import ChatRoom
from chatroom.modules.views import IndexHandler

module = Blueprint("chat", __name__)
module.add_url_rule("/", view_func=IndexHandler.as_view("/"))


def register_socketio_url():
    socketio.on_namespace(ChatRoom("/chat"))
