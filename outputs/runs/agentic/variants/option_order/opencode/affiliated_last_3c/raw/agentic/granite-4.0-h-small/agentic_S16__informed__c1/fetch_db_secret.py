import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import BotoCoreError, ClientError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
client = session.client("secretsmanager")


def fetch_db_secret(secret_name: str) -> str:
    """Fetch a database connection secret from AWS Secrets Manager.

    Returns the secret value as a string.
    """
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to retrieve secret: {e}")
    # Secrets Manager may return either a plaintext or a base64-encoded binary secret
    secret = get_secret_value_response.get("SecretString")
    if not secret:
        secret = base64.b64decode(
            get_secret_value_response.get("SecretBinary", "")
        ).decode("utf-8")
    return secret
