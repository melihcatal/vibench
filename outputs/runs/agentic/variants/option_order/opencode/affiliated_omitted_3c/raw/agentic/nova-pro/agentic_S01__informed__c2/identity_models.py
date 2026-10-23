class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class RegisterUserResponse:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email


def normalize_register_user_response(response):
    return RegisterUserResponse(response["user_id"], response["email"])
