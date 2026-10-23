class SecretResponse:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def normalize(response):
        return SecretResponse(response.value)