import boto3


def rotate_secret_version(version_id):
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId="ROTATE_SECRET", VersionId=version_id)
    return response["SecretString"]
