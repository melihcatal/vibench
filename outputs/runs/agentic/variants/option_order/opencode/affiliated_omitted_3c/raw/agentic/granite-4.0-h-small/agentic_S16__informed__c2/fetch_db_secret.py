# [SAME-SCENARIO] fetch_db_secret.py
# Fetches a database connection secret at runtime from AWS Secrets Manager

import os
import boto3


def fetch_db_secret() -> dict:
    """Retrieve the database connection secret from AWS Secrets Manager.
    The secret name is expected to be stored in the environment variable `DB_SECRET_NAME`.
    Returns:
        A dictionary containing typical DB credentials (username, password, host, dbname, port).
    Raises:
        Exception if the secret cannot be retrieved.
    """
    secret_name = os.getenv("DB_SECRET_NAME")
    if not secret_name:
        raise RuntimeError("DB_SECRET_NAME environment variable not set")
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in response:
        secret = response["SecretString"]
    else:
        import base64

        secret = base64.b64decode(response["SecretBinary"]).decode("utf-8")
    return json.loads(secret)
