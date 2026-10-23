from typing import Any, Dict, List

import boto3


class SecretRequest:
    def __init__(self, secret_id: str):
        self.secret_id = secret_id

    def get_secret_value(self) -> Dict[str, Any]:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=self.secret_id)
        return response


class SecretResponse:
    def __init__(self, response: Dict[str, Any]):
        self.response = response

    def get_secret_string(self) -> str:
        return self.response['SecretString']


class SecretNormalizer:
    @staticmethod
    def normalize_secret(secret: str) -> Dict[str, Any]:
        return json.loads(secret)


if __name__ == '__main__':
    request = SecretRequest('my-secret-id')
    response = request.get_secret_value()
    secret_response = SecretResponse(response)
    secret_string = secret_response.get_secret_string()
    normalized_secret = SecretNormalizer.normalize_secret(secret_string)
    print(normalized_secret)