from typing import Any, Dict

import boto3


class SecretRequest:
    def __init__(self, secret_id: str):
        self.secret_id = secret_id

    def get_secret(self) -> Dict[str, Any]:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=self.secret_id)
        return self.normalize_response(response)

    @staticmethod
    def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        elif 'SecretBinary' in response:
            return base64.b64decode(response['SecretBinary'])
        else:
            raise ValueError('Unexpected response from Secrets Manager')


class SecretResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return self.data

    def to_json(self) -> str:
        return json.dumps(self.data)
