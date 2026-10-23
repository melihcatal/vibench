import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


# Parse JSON Secret
def parse_json_secret(secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.getenv("AZURE_KEY_VAULT_URL"), credential=credential
    )
    secret = client.get_secret(secret_name)
    return json.loads(secret.value)
