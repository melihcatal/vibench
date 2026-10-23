from typing import Any, Dict

import boto3


class SecretRequest:
    def __init__(self, secret_id: str):
        self.secret_id = secret_id

    def get_secret(self) -> Dict[str, Any]:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=self.secret_id)
        return response['SecretString']


class SecretResponse:
    def __init__(self, secret_string: str):
        self.secret_string = secret_string

    def parse_secret(self) -> Dict[str, Any]:
        return json.loads(self.secret_string)


class SecretNormalizer:
    @staticmethod
    def normalize_secret(secret: Dict[str, Any]) -> Dict[str, Any]:
        normalized_secret = {}
        for key, value in secret.items():
            normalized_secret[key.lower()] = value
        return normalized_secret
