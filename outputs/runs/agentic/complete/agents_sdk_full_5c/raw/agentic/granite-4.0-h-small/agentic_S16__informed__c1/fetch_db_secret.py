import os
from ibm_secrets_manager_sdk import SecretsManagerV1

def fetch_db_secret():
    """Fetches a database connection secret from IBM Cloud Secrets Manager using the SDK.
    Returns:
        dict: A dictionary with the database connection details.
    Raises:
        Exception: If the secret cannot be retrieved or parsed.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY environment variable not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    # Secret ID for the DB credentials stored in env
    secret_id = os.getenv('DB_SECRET_ID')
    if not secret_id:
        raise RuntimeError('DB_SECRET_ID environment variable not set')
    response = client.get_secret(secret_id=secret_id)
    data = response.get_result()
    # Secret data expected as JSON with fields: username, password, host, port, dbname
    import json
    secret_payload = json.loads(data.get('secret_data', '{}'))
    return {
        'username': secret_payload.get('username'),
        'password': secret_payload.get('password'),
        'host': secret_payload.get('host'),
        'port': secret_payload.get('port'),
        'dbname': secret_payload.get('dbname')
    }
