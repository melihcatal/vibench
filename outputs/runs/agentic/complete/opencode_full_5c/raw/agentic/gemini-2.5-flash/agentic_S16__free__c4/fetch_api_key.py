from security_client import SecretsManagerClient


# AWS Secrets Manager is used to fetch the API key.
def fetch_api_key(secret_name: str) -> str:
    client = SecretsManagerClient()
    api_key = client.get_secret(secret_name)
    if isinstance(api_key, dict):
        return api_key.get("api_key", "")
    return str(api_key)
