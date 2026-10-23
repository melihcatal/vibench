import json
import os
from botocore.exceptions import NoCredentialsError


def parse_json_secret(secret_name):
    try:
        secret_string = get_secret(secret_name)
        return json.loads(secret_string)
    except NoCredentialsError:
        return "No AWS credentials found"
