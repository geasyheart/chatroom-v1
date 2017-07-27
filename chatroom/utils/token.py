from itsdangerous import TimedJSONWebSignatureSerializer


class Token(object):
    salt = "72339f93598840a8ba3447df6f48e844"

    def __init__(self, secret):
        self.secret = secret

    def dumps(self, obj, salt=None, expires_days=30):
        """
        :type obj: dict
        :param obj: here is dict
        :param salt:
        :param expires_days
        :return: token
        """
        t = TimedJSONWebSignatureSerializer(secret_key=self.secret, expires_in=86400 * expires_days)
        if salt:
            token = t.dumps(obj, salt)
        else:
            token = t.dumps(obj, self.salt)
        if isinstance(token, bytes):
            return token.decode()
        return token

    def loads(self, s, salt=None):
        """
        :type s:str
        :param s: token
        :param salt: 
        :return: None or obj
        """
        t = TimedJSONWebSignatureSerializer(secret_key=self.secret)
        try:
            if salt:
                obj = t.loads(s, salt)
            else:
                obj = t.loads(s, self.salt)
        except:
            return
        else:
            return obj
