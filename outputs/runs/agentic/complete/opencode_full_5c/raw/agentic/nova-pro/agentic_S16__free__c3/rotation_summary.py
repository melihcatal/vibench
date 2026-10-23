import boto3


def summarize_rotation_status():
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.describe_secret(SecretId="ROTATE_SECRET")
    return response["RotationEnabled"]
