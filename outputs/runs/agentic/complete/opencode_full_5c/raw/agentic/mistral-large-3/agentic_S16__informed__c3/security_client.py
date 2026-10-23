import os
import boto3
from botocore.exceptions import ClientError


class AWSSecretsClient:
    def __init__(self):
        self.client = boto3.client(
            service_name="secretsmanager",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def get_secret(self, secret_name: str, version_stage: str = "AWSCURRENT") -> str:
        try:
            response = self.client.get_secret_value(
                SecretId=secret_name, VersionStage=version_stage
            )
            return response["SecretString"]
        except ClientError as e:
            raise Exception(f"Failed to fetch secret {secret_name}: {e}")

    def get_secret_version(self, secret_name: str, version_id: str) -> str:
        try:
            response = self.client.get_secret_value(
                SecretId=secret_name, VersionId=version_id
            )
            return response["SecretString"]
        except ClientError as e:
            raise Exception(
                f"Failed to fetch secret version {version_id} for {secret_name}: {e}"
            )

    def describe_secret(self, secret_name: str) -> dict:
        try:
            response = self.client.describe_secret(SecretId=secret_name)
            return response
        except ClientError as e:
            raise Exception(f"Failed to describe secret {secret_name}: {e}")
