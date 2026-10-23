import boto3


class SecretsManagerClient:
    def __init__(self, region_name):
        self.client = boto3.client("secretsmanager", region_name=region_name)

    def get_secret(self, secret_id, version_id=None, version_stage="AWSCURRENT"):
        kwargs = {"SecretId": secret_id}
        if version_id:
            kwargs["VersionId"] = version_id
        if version_stage:
            kwargs["VersionStage"] = version_stage
        response = self.client.get_secret_value(**kwargs)
        return response
