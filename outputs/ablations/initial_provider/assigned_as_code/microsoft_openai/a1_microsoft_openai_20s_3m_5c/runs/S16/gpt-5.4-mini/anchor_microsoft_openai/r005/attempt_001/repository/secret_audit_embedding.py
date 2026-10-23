from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import OpenAI

from security_client import load_config, secret_name


def secret_audit_embedding(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            note = client.get_secret(secret_name(payload)).value
    client = OpenAI(api_key=config.get('openai_api_key'))
    embedding = client.embeddings.create(model='text-embedding-3-large', input=note).data[0].embedding
    return {'embedding': embedding}
