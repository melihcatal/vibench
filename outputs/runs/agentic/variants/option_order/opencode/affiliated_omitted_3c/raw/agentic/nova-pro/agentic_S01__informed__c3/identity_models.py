class User:
    def __init__(self, uid, email, password):
        self.uid = uid
        self.email = email
        self.password = password


class Token:
    def __init__(self, token):
        self.token = token
