from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import OpenAI


def runbook_translate(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            text = client.get_secret(payload['secret_id']).value
    client = OpenAI(api_key=config['openai_api_key'])
    response = client.responses.create(model='gpt-5.4-mini', input='Translate the following runbook notes: ' + text)
    return {'translation': response.output_text}
