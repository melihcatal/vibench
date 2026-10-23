from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from google.cloud import translate


def translate_secret_rotation_runbook(payload):
    credential = DefaultAzureCredential()
    key_vault_client = SecretClient(vault_url=payload['vault_url'], credential=credential)
    secret = key_vault_client.get_secret(payload['secret_name'])
    translate_client = translate.TranslationServiceClient()
    parent = f'projects/{payload['project_id']}'
    response = translate_client.translate_text(parent, text=secret.value, target_language_code=payload['target_language'])
    translated_text = response.translations[0].translated_text
    return {'translated_runbook': translated_text}