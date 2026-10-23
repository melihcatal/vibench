class SecretRequest:
    def __init__(self, secret_name):
        self.secret_name = secret_name

class SecretResponse:
    def __init__(self, secret_value):
        self.secret_value = secret_value