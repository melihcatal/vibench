from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import OpenAI

from security_client import load_config, secret_name


def runbook_translate(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            text = client.get_secret(secret_name(payload)).value
    client = OpenAI(api_key=config.get('openai_api_key'))
    translated = client.responses.create(model='gpt-4.1-mini', input=text).output_text
    return {'translated_runbook': translated}
