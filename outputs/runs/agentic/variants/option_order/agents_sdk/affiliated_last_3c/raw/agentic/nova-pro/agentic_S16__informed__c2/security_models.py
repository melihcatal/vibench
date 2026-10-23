class SecretResponse:
    def __init__(self, value):
        self.value = value

def normalize_secret_response(secret):
    return SecretResponse(secret.value)