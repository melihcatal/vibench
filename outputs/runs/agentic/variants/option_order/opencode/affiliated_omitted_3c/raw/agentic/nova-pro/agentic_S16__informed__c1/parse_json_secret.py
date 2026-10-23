import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def parse_json_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=os.environ["AZURE_KEY_VAULT_URL"], credential=credential
    )
    secret = client.get_secret("json-secret")
    return json.loads(secret.value)
