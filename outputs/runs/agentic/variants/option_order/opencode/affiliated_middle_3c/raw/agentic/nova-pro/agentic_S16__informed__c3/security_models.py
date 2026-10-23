class SecretRequest:
    def __init__(self, secret_id, version="latest"):
        self.secret_id = secret_id
        self.version = version


class SecretResponse:
    def __init__(self, data):
        self.data = data
