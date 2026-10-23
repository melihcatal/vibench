import boto3
from typing import Dict, List


class SecretRotationSummarizer:
    def __init__(self):
        self.client = boto3.client(
            "secretsmanager",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def rotation_summary(self, secret_name: str) -> Dict[str, Any]:
        response = self.client.describe_secret(SecretId=secret_name)
        return {
            "name": response.get("Name"),
            "rotation_enabled": response.get("RotationEnabled", False),
            "last_rotated_date": str(response.get("LastRotatedDate", "")),
            "last_changed_date": str(response.get("LastChangedDate", "")),
            "next_rotation_date": str(response.get("NextRotationDate", "")),
            "rotation_lambda_arn": response.get("RotationLambdaARN", ""),
        }
