import os

import boto3


def rotation_summary():
    client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    secret_id = os.getenv("AWS_ROTATION_SUMMARY_SECRET_ID", "rotation/secret")
    metadata = client.describe_secret(SecretId=secret_id)
    return {"secret_id": secret_id, "rotation_enabled": metadata.get("RotationEnabled", False), "rotation_rules": metadata.get("RotationRules", {}), "last_changed_date": str(metadata.get("LastChangedDate", ""))}


if __name__ == "__main__":
    print(rotation_summary())
