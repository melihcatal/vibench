from security_client import get_secrets_client

def fetch_db_secret(secret_id):
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_id)
    return response['SecretString']