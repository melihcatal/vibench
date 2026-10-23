from security_client import get_aws_secrets_client
from security_models import ApiKeySecret

def fetch_api_key(secret_id: str) -> str:
    client = get_aws_secrets_client()
    response = client.get_secret_value(SecretId=secret_id)
    secret_string = response['SecretString']
    api_key_secret = ApiKeySecret.model_validate_json(secret_string)
    return api_key_secret.api_key
