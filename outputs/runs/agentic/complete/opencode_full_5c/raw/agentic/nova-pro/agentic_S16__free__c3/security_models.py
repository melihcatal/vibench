class SecretRequest:
    def __init__(self, secret_id):
        self.secret_id = secret_id


class SecretResponse:
    def __init__(self, secret_string):
        self.secret_string = secret_string
