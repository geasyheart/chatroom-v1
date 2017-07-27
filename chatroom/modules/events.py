from flask import request, current_app
from flask_socketio import emit, Namespace, join_room, disconnect

from chatroom.models.user import ChatUser, ChatSidUser, ChatUserRole, ChatSidRoom, ChatUserCount, UserBlock
from chatroom.utils.log import get_logger
from chatroom.utils.token import Token

logger = get_logger()


class ChatRoom(Namespace):
    def on_connect(self):
        count = ChatUserCount.inc_count()
        if count > current_app.config.get("LIMIT_SIZE", 1000):
            disconnect()
        msg = '建立了新连接'.center(60, '-')
        logger.info(msg)

    def on_join(self, message):
        sid = request.sid
        room = message.get('room')
        token = message.get('token')
        if not room: disconnect()
        if not token: disconnect()
        token_obj = Token(current_app.config['SECRET_KEY'])
        obj = token_obj.loads(token)  # type: dict
        if not obj: disconnect()
        uid, role = obj["uid"], obj["role"]
        # ##########block################
        user_block = UserBlock(uid)
        block_global = user_block.is_block()
        if block_global: disconnect()
        block_room = user_block.is_block(room)
        if block_room: disconnect()
        # ############user###############
        chat_user = ChatUser(uid, sid)
        exist = chat_user.get_room_uid(room)
        logger.error("此处判断是否存在:{}".format(exist))
        if exist: disconnect()
        ChatSidUser.sid_uid_map(sid, uid)
        ChatUserRole.uid_role_map(uid, role)
        ChatSidRoom.sid_room_map(sid, room)

        chat_user.connect(room)

        join_room(room)
        msg = "{}加入了房间{}".format(uid, room).center(60, '-')
        logger.info(msg)
        emit("status", {"message": msg}, room=room)

    def on_message(self, message):
        sid = request.sid
        uid = ChatSidUser.get_uid(sid)
        room = ChatSidRoom.get_room(sid)
        # ##########block################
        user_block = UserBlock(uid)
        block_global = user_block.is_block()
        if block_global: disconnect()
        block_room = user_block.is_block(room)
        if block_room: disconnect()
        # ##########################
        msg = "{}在房间{}发送{}".format(uid, room, message)
        logger.info(msg)
        emit('status', {"message": msg}, room=room)

    def on_user(self, message):
        """
        统计当前在线用户
        :param message: 
        :return: 
        """

        sid = request.sid
        room = ChatSidRoom.get_room(sid)
        if room:
            logger.info("当前room:{}".format(room).center(60, '-'))
            active_user = ChatUser.active_user(room)
            logger.info(active_user)
            emit('active_user', {'message': active_user}, room=room)

    def on_disconnect(self):
        logger.info('disconnect'.center(60, '-'))
        sid = request.sid
        ChatUserCount.dec_count()
        room = ChatSidRoom.get_room(sid)
        if room:
            uid = ChatSidUser.get_uid(sid)
            chat_user = ChatUser(uid, sid)
            chat_user.disconnect(room)
            msg = '{}离开了房间{}'.format(uid, room).center(60, '-')
            logger.info(msg)
            ChatUserRole.delete_map(uid)
            emit('status', {"message": msg}, room=room)
            #  表示未连接就已经断开
