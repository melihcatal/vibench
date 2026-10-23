class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class RegisterUserResponse:
    def __init__(self, json_response):
        self.json_response = json_response
