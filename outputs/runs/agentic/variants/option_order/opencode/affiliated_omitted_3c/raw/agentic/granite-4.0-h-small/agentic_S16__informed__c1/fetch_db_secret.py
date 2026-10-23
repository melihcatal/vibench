import os
import json

# AWS Secrets Manager integration
import boto3

# Configuration (normally loaded from env or config file)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DB_SECRET_NAME = "my-db-connection"


def fetch_db_secret() -> dict:
    """Fetches a database connection secret from AWS Secrets Manager.
    Returns:
        A dictionary containing the secret fields (e.g., username, password, host).
    Raises:
        RuntimeError: If the secret cannot be retrieved.
    """
    client = boto3.client(service_name="secretsmanager", region_name=AWS_REGION)
    response = client.get_secret_value(SecretId=DB_SECRET_NAME)
    # The secret value is stored as a JSON string in the 'SecretString' field
    return json.loads(response["SecretString"])
