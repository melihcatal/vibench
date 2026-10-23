import os
import boto3
from security_models import RotationSummary


def rotation_summary(secret_name: str) -> RotationSummary:
    client = boto3.client(
        service_name="secretsmanager", region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    response = client.describe_secret(SecretId=secret_name)

    return RotationSummary(
        secret_name=secret_name,
        current_version=response.get("VersionIdsToStages", {}).get(
            "AWSCURRENT", [None]
        )[0],
        previous_version=response.get("VersionIdsToStages", {}).get(
            "AWSPREVIOUS", [None]
        )[0],
        rotation_enabled=response.get("RotationEnabled", False),
        last_rotation_date=response.get("LastRotatedDate", None),
        next_rotation_date=response.get("NextRotationDate", None),
    )
