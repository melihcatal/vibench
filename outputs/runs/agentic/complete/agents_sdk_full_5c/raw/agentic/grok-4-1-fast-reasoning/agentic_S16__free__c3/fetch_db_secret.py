import json
import os
from security_client import get_secrets_client
from security_models import DBConnectionSecret

def fetch_db_secret(secret_name: str = None) -&gt; DBConnectionSecret:
    if secret_name is None:
        secret_name = os.getenv('DB_SECRET_NAME')
    if not secret_name:
        raise ValueError('DB_SECRET_NAME must be set')
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_name)
    secret_dict = json.loads(response['SecretString'])
    return DBConnectionSecret.model_validate(secret_dict)