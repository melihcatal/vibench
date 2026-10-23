import os

import boto3

class AWSSecretsManagerClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("secretsmanager", region_name=self.region_name)

    def get_secret_value(self, secret_id: str, version_id: str = None, version_stage: str = None):
        kwargs = {"SecretId": secret_id}
        if version_id:
            kwargs["VersionId"] = version_id
        if version_stage:
            kwargs["VersionStage"] = version_stage

        response = self.client.get_secret_value(**kwargs)
        if "SecretString" in response:
            return response["SecretString"]
        elif "SecretBinary" in response:
            return response["SecretBinary"].decode("utf-8")
        return None

    def describe_secret(self, secret_id: str):
        return self.client.describe_secret(SecretId=secret_id)

    def list_secrets(self):
        return self.client.list_secrets()

    def update_secret_version_stage(self, secret_id: str, version_stage: str, secret_version_id: str):
        return self.client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage=version_stage,
            MoveToVersionId=secret_version_id
        )
