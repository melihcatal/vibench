# parse_json_secret.py
# [SAME-SCENARIO]
# Retrieves and parses a JSON-formatted secret (Google Secret Manager)
import os
from google.cloud import secretmanager
import json

from security_client import get_secret_manager_client

def parse_json_secret(secret_name: str = os.getenv('JSON_SECRET')) -> dict:
    """Fetch a secret that contains JSON data and parse it into a dict.",
    client = get_secret_manager_client()
    response = client.access_secret_version(name=f'projects/-/secrets/{secret_name}/versions/latest')
    payload = response.payload.data.decode('UTF-8')
    return json.loads(payload)

if __name__ == '__main__':
    secret_dict = parse_json_secret()
    print('Parsed secret JSON:', secret_dict)