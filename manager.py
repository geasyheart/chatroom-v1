import click

from chatroom import create_app
from chatroom.ext.socketio_init import socketio
import eventlet

eventlet.monkey_patch()


@click.group()
def command():
    pass


@command.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, debug, host, port):
    """Run the Flask development server i.e. app.run()"""
    app = create_app(api_server=True)
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


@command.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def run_socketio_server(reloader, debug, host, port):
    app = create_app()
    socketio.run(app, host=host, port=port)


manager = click.CommandCollection()
manager.add_source(command)

if __name__ == "__main__":
    manager()
