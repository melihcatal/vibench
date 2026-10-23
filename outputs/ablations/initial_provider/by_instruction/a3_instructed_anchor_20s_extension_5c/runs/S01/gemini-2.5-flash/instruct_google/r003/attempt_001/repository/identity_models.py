
class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class RegisterUserResponse:
    def __init__(self, uid, email, display_name=None):
        self.uid = uid
        self.email = email
        self.display_name = display_name
