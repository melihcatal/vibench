class IdentityRequest:
    def __init__(self, scopes):
        self.scopes = scopes

class IdentityResponse:
    def __init__(self, tokens):
        self.tokens = tokens