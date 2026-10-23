from security_client import get_secret_client, get_secret_name
from security_models import SecretRequest, parse_json_payload

client = get_secret_client('aws')
request = SecretRequest(secret_name=get_secret_name('DB_SECRET_NAME', 'service/database'))
response = client.get_secret_value(SecretId=request.secret_name)
secret = parse_json_payload(response.get('SecretString') or response.get('SecretBinary'))
print(secret.get('connection_string', ''))
