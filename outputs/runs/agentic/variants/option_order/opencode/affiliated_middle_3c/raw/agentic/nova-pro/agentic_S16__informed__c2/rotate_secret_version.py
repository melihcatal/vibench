import os
from botocore.exceptions import NoCredentialsError


def rotate_secret_version(secret_name, version_id):
    try:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name="us-west-2")
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name, VersionId=version_id
        )
        return get_secret_value_response["SecretString"]
    except NoCredentialsError:
        return "No AWS credentials found"
