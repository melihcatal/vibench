import boto3

from security_client import aws_client_kwargs, secret_name, secret_version_stage
from security_models import rotation_payload


def rotate_secret_version(version_id=None, stage=None):
    client = boto3.client("secretsmanager", **aws_client_kwargs())
    params = {"SecretId": secret_name("rotation/secret")}
    params.update(rotation_payload(version_id, stage or secret_version_stage()))
    return client.get_secret_value(**params)
