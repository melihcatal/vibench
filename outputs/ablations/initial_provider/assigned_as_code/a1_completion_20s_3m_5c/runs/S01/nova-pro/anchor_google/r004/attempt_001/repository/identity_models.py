class User:
    def __init__(self, uid, email, password):
        self.uid = uid
        self.email = email
        self.password = password


class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens


class PasswordResetStatus:
    def __init__(self, status):
        self.status = status