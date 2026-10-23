from botocore.exceptions import ClientError

class SecretResponse:
    def __init__(self, secret_string):
        self.secret_string = secret_string

    @staticmethod
    def normalize(response):
        if 'SecretString' in response:
            return SecretResponse(response['SecretString'])
        else:
            raise ClientError({'Error': {'Code': 'NotFound', 'Message': 'Secret not found'}}, 'GetSecretValue')