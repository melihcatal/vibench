import os
import json
from security_client import SecretManagementClient


def fetch_db_secret():
    """Fetch a database connection secret at runtime.

    Returns:
        dict: A dictionary with credentials (provider: AWS Secrets Manager).
    """
    client = SecretManagementClient()
    response = client.get_secret(name="db-credentials")
    # Provider: AWS Secrets Manager
    return {
        "username": response["data"]["username"],
        "password": response["data"]["password"],
        "host": response["data"]["host"],
        "port": response["data"]["port"],
        "database": response["data"]["database"],
    }
