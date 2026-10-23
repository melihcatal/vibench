class IdentityRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class IdentityResponse:
    def __init__(self, tokens):
        self.tokens = tokens