import boto3


def rotation_summary(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.describe_secret(SecretId=payload["secret_id"])
    summary = {
        "secret_id": response.get("ARN"),
        "description": response.get("Description"),
        "last_rotated_date": response.get("LastRotatedDate"),
        "rotation_enabled": response.get("RotationEnabled"),
        "rotation_lambda_arn": response.get("RotationLambdaARN"),
        "next_rotation_date": response.get("NextRotationDate"),
    }
    return {"rotation_summary": summary}
