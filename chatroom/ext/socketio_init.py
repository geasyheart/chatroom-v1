from flask_socketio import SocketIO

from chatroom.utils.log import get_logger

socketio = SocketIO(async_mode="eventlet", logger=True, engineio_logger=True)

logger = get_logger()


def configure(app):
    message_queue = app.config.get("MESSAGE_QUEUE")
    if message_queue:
        socketio.init_app(app, message_queue=message_queue)
    else:
        socketio.init_app(app)

    @socketio.on_error()  # Handles the default namespace
    def error_handler(e):
        logger.error(str(e))

    @socketio.on_error('/chat')  # handles the '/chat' namespace
    def error_handler_chat(e):
        logger.error(str(e))

    @socketio.on_error_default  # handles all namespaces without an explicit error handler
    def default_error_handler(e):
        logger.error(str(e))
