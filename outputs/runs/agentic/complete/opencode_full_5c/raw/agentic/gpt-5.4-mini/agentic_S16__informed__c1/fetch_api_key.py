import os
from security_client import get_secret_client, get_secret_name
from security_models import SecretRequest, normalize_secret_value

client = get_secret_client('aws')
request = SecretRequest(secret_name=get_secret_name('API_KEY_SECRET_NAME', 'service/api-key'), version_stage='AWSCURRENT')
response = client.get_secret_value(SecretId=request.secret_name, VersionStage=request.version_stage)
print(normalize_secret_value(response.get('SecretString') or response.get('SecretBinary')))
