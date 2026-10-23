import json
from security_client import get_secrets_client

def parse_json_secret(secret_id):
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_id)
    return json.loads(response['SecretString'])