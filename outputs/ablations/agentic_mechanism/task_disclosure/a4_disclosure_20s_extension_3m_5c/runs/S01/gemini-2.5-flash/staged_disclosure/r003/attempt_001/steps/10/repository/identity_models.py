
class EmailPasswordSignUpRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordSignUpResponse:
    def __init__(self, user_id, email, status):
        self.user_id = user_id
        self.email = email
        self.status = status

class EmailPasswordSignInRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordSignInResponse:
    def __init__(self, user_id, email, token, status):
        self.user_id = user_id
        self.email = email
        self.token = token
        self.status = status

class EmailPasswordNormalizationHelper:
    @staticmethod
    def normalize_email(email):
        return email.lower().strip()
