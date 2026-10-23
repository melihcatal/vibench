class SignUpResponse:
    def __init__(self, user_confirmed, code_delivery_details):
        self.user_confirmed = user_confirmed
        self.code_delivery_details = code_delivery_details

class InitiateAuthResponse:
    def __init__(self, authentication_result):
        self.authentication_result = authentication_result

class ForgotPasswordResponse:
    def __init__(self, code_delivery_details):
        self.code_delivery_details = code_delivery_details