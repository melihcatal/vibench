import json
from typing import cast
from security_client import get_secrets_client
from security_models import DbConnectionSecret, parse_json_secret


def fetch_db_secret(secret_name: str) -> DbConnectionSecret:
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_name)
    data = parse_json_secret(response["SecretString"])
    return cast(DbConnectionSecret, data)
