class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class RegisterUserResponse:
    def __init__(self, user_sub, code_delivery_details):
        self.user_sub = user_sub
        self.code_delivery_details = code_delivery_details
