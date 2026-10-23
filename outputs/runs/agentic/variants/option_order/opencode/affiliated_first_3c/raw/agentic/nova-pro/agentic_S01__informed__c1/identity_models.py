class SignUpRequest:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class SignUpResponse:
    def __init__(self, user_id):
        self.user_id = user_id
