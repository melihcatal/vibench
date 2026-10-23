from aws_amplify import Auth

class EmailPasswordRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def validate(request):
        if not request.email or not request.password:
            raise ValueError('Email and password are required')

class EmailPasswordResponse:
    def __init__(self, tokens):
        self.tokens = tokens

    @staticmethod
    def normalize(response):
        if not response or not response.tokens:
            raise ValueError('Invalid response')
        return response

