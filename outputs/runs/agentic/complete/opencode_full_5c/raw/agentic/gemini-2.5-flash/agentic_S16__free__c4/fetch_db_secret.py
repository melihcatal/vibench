import json
from security_client import SecretsManagerClient


# AWS Secrets Manager is used to fetch the database connection secret.
def fetch_db_secret(secret_name: str) -> dict:
    client = SecretsManagerClient()
    secret_value = client.get_secret(secret_name)
    if isinstance(secret_value, str):
        return json.loads(secret_value)
    return secret_value
