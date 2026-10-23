class SecretRequest:
    def __init__(self, secret_name):
        self.secret_name = secret_name


class SecretResponse:
    def __init__(self, secret_string):
        self.secret_string = secret_string
