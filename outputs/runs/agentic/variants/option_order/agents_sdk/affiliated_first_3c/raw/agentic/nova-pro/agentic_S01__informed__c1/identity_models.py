class SignUpResponse:
    def __init__(self, user_confirmed, code_delivery_details):
        self.user_confirmed = user_confirmed
        self.code_delivery_details = code_delivery_details

class InitiateAuthResponse:
    def __init__(self, authentication_result, challenge_name=None):
        self.authentication_result = authentication_result
        self.challenge_name = challenge_name