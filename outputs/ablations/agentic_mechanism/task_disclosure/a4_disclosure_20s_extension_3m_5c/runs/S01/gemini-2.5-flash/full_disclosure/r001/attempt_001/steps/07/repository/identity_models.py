class SignUpRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class SignUpResponse:
    def __init__(self, user_id, email, access_token, refresh_token):
        self.user_id = user_id
        self.email = email
        self.access_token = access_token
        self.refresh_token = refresh_token

class SignInRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class SignInResponse:
    def __init__(self, user_id, email, access_token, refresh_token):
        self.user_id = user_id
        self.email = email
        self.access_token = access_token
        self.refresh_token = refresh_token

class RefreshSessionRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class RefreshSessionResponse:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

class PasswordResetRequest:
    def __init__(self, email):
        self.email = email

class PasswordResetResponse:
    def __init__(self, message):
        self.message = message

def normalize_email(email):
    return email.lower().strip()
