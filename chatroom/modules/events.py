from flask_socketio import emit, Namespace, join_room
from flask import request, session


class ChatRoom(Namespace):
    def on_connect(self):
        sid = request.sid
        emit('sid', {"message": "{}".format(sid)})

    def on_join(self, message):
        sid = request.sid
        room = message.get('room')
        session['room'] = room
        if not room: room = 'room1'
        join_room(room)
        emit("status", {"message": "{}加入房间".format(sid)}, room=room)

    def on_message(self, message):
        sid = request.sid
        message.update({"sid": sid})
        room = session['room']
        emit('status', {"message": str(message)}, room=room)
