from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import OpenAI


def secret_audit_embedding(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            note = client.get_secret(payload['secret_id']).value
    client = OpenAI(api_key=config['openai_api_key'])
    response = client.embeddings.create(model='text-embedding-3-small', input=note)
    return {'embedding': response.data[0].embedding}
