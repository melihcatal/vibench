class SignUpResponse:
    def __init__(self, user_confirmed, user_sub):
        self.user_confirmed = user_confirmed
        self.user_sub = user_sub

class InitAuthResponse:
    def __init__(self, authentication_result):
        self.authentication_result = authentication_result