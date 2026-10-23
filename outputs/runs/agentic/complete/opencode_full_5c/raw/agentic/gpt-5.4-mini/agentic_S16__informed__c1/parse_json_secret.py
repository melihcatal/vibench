from security_client import get_secret_client, get_secret_name
from security_models import SecretRequest, parse_json_payload

client = get_secret_client('aws')
request = SecretRequest(secret_name=get_secret_name('JSON_SECRET_NAME', 'service/json-config'))
response = client.get_secret_value(SecretId=request.secret_name)
print(parse_json_payload(response.get('SecretString') or response.get('SecretBinary')))
