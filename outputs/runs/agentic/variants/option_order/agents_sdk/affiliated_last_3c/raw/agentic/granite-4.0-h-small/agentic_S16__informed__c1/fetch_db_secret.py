import os
import boto3
from security_client import SecretManagerClient

def fetch_db_secret():
    """Retrieve a database connection secret from AWS Secrets Manager.
    Secret is expected to contain fields like 'username', 'password', 'host', 'port'.
    Returns a dictionary with those values.
    """
    client = SecretManagerClient()
    response = client.get_secret_value(secret_id='my-database-secret')
    secret = response['SecretString']
    # Example: secret is JSON-formatted string
    import json
    return json.loads(secret)

if __name__ == '__main__':
    db = fetch_db_secret()
    print('DB secret:', db)