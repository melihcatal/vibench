import boto3

from.security_models import NormalizeResponse


class SecurityClient:
    def __init__(self, region_name=None):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret_value(self, secret_id):
        response = self.client.get_secret_value(SecretId=secret_id)
        return NormalizeResponse(response)