class UserRegistrationRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserRegistrationResponse:
    def __init__(self, object_id):
        self.object_id = object_id