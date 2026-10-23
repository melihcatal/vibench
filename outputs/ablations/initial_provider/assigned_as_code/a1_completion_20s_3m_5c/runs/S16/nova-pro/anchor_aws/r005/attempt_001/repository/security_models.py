class NormalizeResponse:
    def __init__(self, response):
        self.response = response

    def get_secret_string(self):
        return self.response['SecretString'] if 'SecretString' in self.response else self.response['SecretBinary'].decode('utf-8')