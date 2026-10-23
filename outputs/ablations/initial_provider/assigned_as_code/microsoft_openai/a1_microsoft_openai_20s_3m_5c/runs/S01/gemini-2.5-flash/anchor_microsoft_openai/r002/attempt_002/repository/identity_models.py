class UserRegistrationPayload:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserLoginPayload:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class TokenRefreshPayload:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class PasswordResetPayload:
    def __init__(self, email):
        self.email = email

class UserProfile:
    def __init__(self, user_id, display_name, email):
        self.user_id = user_id
        self.display_name = display_name
        self.email = email

class AuthTokens:
    def __init__(self, access_token, refresh_token=None, expires_in=None, token_type="Bearer"):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
