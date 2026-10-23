import json
import os
from google.cloud import secretmanager

def parse_json_secret(payload, config=None):
    config = config or {}
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    secret_id = payload['secret_id']
    version_id = payload.get('version_id', 'latest')

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={'name': name})
    
    secret_string = response.payload.data.decode('UTF-8')
    
    if payload.get('key_field'):
        parsed_secret = json.loads(secret_string)
        return {payload['key_field']: parsed_secret.get(payload['key_field'])}
    
    return {'parsed_secret': json.loads(secret_string)}
