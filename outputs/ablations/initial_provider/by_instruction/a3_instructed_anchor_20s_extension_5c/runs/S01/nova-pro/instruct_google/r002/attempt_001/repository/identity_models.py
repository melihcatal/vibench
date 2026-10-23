class User:
    def __init__(self, uid, email, password):
        self.uid = uid
        self.email = email
        self.password = password

class AuthToken:
    def __init__(self, id_token, refresh_token):
        self.id_token = id_token
        self.refresh_token = refresh_token