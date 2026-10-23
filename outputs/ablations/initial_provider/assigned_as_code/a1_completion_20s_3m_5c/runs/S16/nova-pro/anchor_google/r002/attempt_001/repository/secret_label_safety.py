from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def check_secret_label_safety(payload):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=payload['vault_url'], credential=credential)
    secret = client.get_secret(payload['secret_name'])
    unsafe_keywords = ['password', 'secret', 'key']
    is_safe = all(keyword not in secret.name for keyword in unsafe_keywords)
    return {'is_safe': is_safe}