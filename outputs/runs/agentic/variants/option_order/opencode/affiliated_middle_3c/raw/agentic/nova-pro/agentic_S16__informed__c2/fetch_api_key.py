import os
from botocore.exceptions import NoCredentialsError


def get_secret(secret_name):
    try:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name="us-west-2")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response["SecretString"]
    except NoCredentialsError:
        return "No AWS credentials found"
