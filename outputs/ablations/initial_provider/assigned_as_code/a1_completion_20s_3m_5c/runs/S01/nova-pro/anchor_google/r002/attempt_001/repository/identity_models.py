class IdentityRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class IdentityResponse:
    def __init__(self, user_id):
        self.user_id = user_id


def normalize_response(response):
    return IdentityResponse(response["user_id"])
