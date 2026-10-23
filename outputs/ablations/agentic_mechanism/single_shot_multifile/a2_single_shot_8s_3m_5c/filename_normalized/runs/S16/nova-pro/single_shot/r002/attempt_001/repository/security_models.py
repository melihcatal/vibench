class SecretResponse:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def normalize(secret):
        return SecretResponse(secret.value)