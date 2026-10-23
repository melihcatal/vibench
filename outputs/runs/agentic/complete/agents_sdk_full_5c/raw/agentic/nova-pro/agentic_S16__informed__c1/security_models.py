class SecretResponse:
    def __init__(self, secret_string):
        self.secret_string = secret_string

    @staticmethod
    def normalize_response(response):
        return SecretResponse(response['SecretString'])