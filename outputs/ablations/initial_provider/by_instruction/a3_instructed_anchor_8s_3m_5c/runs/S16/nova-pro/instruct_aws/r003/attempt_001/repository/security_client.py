import boto3

class SecurityClient:
    def __init__(self):
        self.client = boto3.client('secretsmanager')

    def get_secret(self, secret_name):
        get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response['SecretString']