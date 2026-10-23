import boto3
import json
import os


class AWSSecretsManagerClient:
    def __init__(self):
        self.client = boto3.client(
            "secretsmanager",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def parse_json_secret(self, secret_id: str) -> dict:
        response = self.client.get_secret_value(SecretId=secret_id)
        return json.loads(response["SecretString"])
