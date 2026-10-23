import json

import boto3


def fetch_db_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    secret_string = response["SecretString"]
    db_secret = json.loads(secret_string)
    return {
        "host": db_secret.get("host"),
        "port": db_secret.get("port"),
        "username": db_secret.get("username"),
        "password": db_secret.get("password"),
        "dbname": db_secret.get("dbname"),
    }
