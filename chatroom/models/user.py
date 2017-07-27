from chatroom.ext.redis_init import redis_db
from chatroom.utils.date_time import DateTime


def utf8(content):
    if isinstance(content, bytes):
        return content.decode()
    elif isinstance(content, str):
        return content
    else:
        return


class ChatSidUser(object):
    """管理user sid"""
    SID_USER_PREFIX = "chat:sid:uid"

    @classmethod
    def sid_uid_map(cls, sid, uid):
        redis_db.hset(cls.SID_USER_PREFIX, sid, uid)

    @classmethod
    def get_uid(cls, sid):
        uid = redis_db.hget(cls.SID_USER_PREFIX, sid)
        if uid is None:
            return
        return uid


class ChatSidRoom(object):
    SID_ROOM_PREFIX = "chat:sid:room"

    @classmethod
    def sid_room_map(cls, sid, room):
        redis_db.hset(cls.SID_ROOM_PREFIX, sid, room)

    @classmethod
    def get_room(cls, sid):
        return utf8(redis_db.hget(cls.SID_ROOM_PREFIX, sid))


class ChatUserRole(object):
    """映射uid role"""
    USER_ROLE_PREFIX = "chat:uid:role"

    @classmethod
    def uid_role_map(cls, uid, role):
        redis_db.hset(cls.USER_ROLE_PREFIX, uid, role)

    @classmethod
    def delete_map(cls, uid):
        redis_db.hdel(cls.USER_ROLE_PREFIX, uid)


class ChatUserCount(object):
    """存放实际所有在线人数"""
    USER_COUNT_PREFIX = "chat:uid:count:{}"

    @classmethod
    def get_count(cls):
        key = cls.USER_COUNT_PREFIX.format(DateTime.today())
        return redis_db.get(key)

    @classmethod
    def inc_count(cls):
        key = cls.USER_COUNT_PREFIX.format(DateTime.today())
        return redis_db.incr(key)

    @classmethod
    def dec_count(cls):
        key = cls.USER_COUNT_PREFIX.format(DateTime.today())
        return redis_db.decr(key)


class ChatUser(object):
    """管理chat user"""
    ROOM_USER_PREFIX = "chat:room:{}:uid"  # 保存此room所有active user:sid
    ROOM_USER_PING_PREFIX = "chat:room:{}:ping"  # 保存此room所有已经断线的user

    TIMEOUT = 10  # 超时时长

    def __init__(self, uid, sid):
        self.uid = uid
        self.sid = sid

    def connect(self, room):
        # 添加active user
        room = utf8(room)
        room_key = self.ROOM_USER_PREFIX.format(room)
        room_ping_key = self.ROOM_USER_PING_PREFIX.format(room)
        redis_db.hset(room_key, self.uid, self.sid)
        redis_db.hdel(room_ping_key, self.uid)

    def disconnect(self, room):
        # 添加离线用户到临时表
        room = utf8(room)
        room_key = self.ROOM_USER_PREFIX.format(room)
        room_ping_key = self.ROOM_USER_PING_PREFIX.format(room)
        redis_db.hdel(room_key, self.uid)
        redis_db.hset(room_ping_key, self.uid, DateTime.timestamp() + self.TIMEOUT)

    def get_room_uid(self, room):
        """
        判断此房间是否已经有此uid
        :param room: 
        :return: 
        """
        room = utf8(room)
        room_key = self.ROOM_USER_PREFIX.format(room)
        exist = redis_db.hget(room_key, self.uid)
        if exist:
            return True
        return False

    @classmethod
    def active_user(cls, room):
        uids = []
        room = utf8(room)
        # 获取当前active user
        room_key = cls.ROOM_USER_PREFIX.format(room)
        room_ping_key = cls.ROOM_USER_PING_PREFIX.format(room)
        ping_user = redis_db.hgetall(room_ping_key)
        now = DateTime.timestamp()
        if ping_user:
            for _uid, _time in ping_user.items():
                if now < int(_time):
                    uids.append(int(_uid))
        keys = [int(i) for i in redis_db.hkeys(room_key)]
        uids.extend(keys)
        return uids


class UserBlock(object):
    GLOBAL_BLOCK = "chat:block:global"
    BLOCK_ROOM_USER = "chat:block:room:{}"

    def __init__(self, uid):
        """
        
        :param uid: 
        
        """
        self.uid = uid

    def block(self, room=None):
        """
        如果不传room,则全局block
        :param room
        :return: 
        """
        timestamp = DateTime.timestamp()
        if room is None:
            redis_db.hset(self.GLOBAL_BLOCK, self.uid, timestamp)
        else:
            block_room = self.BLOCK_ROOM_USER.format(room)
            redis_db.hset(block_room, self.uid, timestamp)

    def unblock(self, room):
        """
        取消block
        :param room: 
        """
        if room is None:
            redis_db.hdel(self.GLOBAL_BLOCK, self.uid)
        else:
            block_room = self.BLOCK_ROOM_USER.format(room)
            redis_db.hdel(block_room, self.uid)

    def is_block(self, room=None):
        """
        判断是否block
        :param room: 
        """
        if room is None:
            b = redis_db.hget(self.GLOBAL_BLOCK, self.uid)
            if b: return True
        else:
            block_room = self.BLOCK_ROOM_USER.format(room)
            b = redis_db.hget(block_room, self.uid)
            if b: return True
        return False

    def list_block(self):
        """返回block列表"""
        raise NotImplementedError
