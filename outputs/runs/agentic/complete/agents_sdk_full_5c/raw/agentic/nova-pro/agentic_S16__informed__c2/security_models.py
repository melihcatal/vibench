class SecretRequest:
    def __init__(self, name):
        self.name = name

class SecretResponse:
    def __init__(self, value):
        self.value = value

def normalize_secret_response(response):
    return SecretResponse(response.value)