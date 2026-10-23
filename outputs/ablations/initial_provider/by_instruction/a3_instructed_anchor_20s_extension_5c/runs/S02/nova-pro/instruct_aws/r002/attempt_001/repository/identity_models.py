class AuthRequest:
    def __init__(self, client_id, redirect_uri, scope, response_type, code_challenge=None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.response_type = response_type
        self.code_challenge = code_challenge

class AuthResponse:
    def __init__(self, authorization_code):
        self.authorization_code = authorization_code

class UserProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email