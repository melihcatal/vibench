import json

import boto3


def fetch_db_secret(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"])
    secret_string = response["SecretString"]
    db_credentials = json.loads(secret_string)
    return {
        "username": db_credentials.get("username"),
        "password": db_credentials.get("password"),
        "host": db_credentials.get("host"),
        "port": db_credentials.get("port"),
        "dbname": db_credentials.get("dbname"),
    }
