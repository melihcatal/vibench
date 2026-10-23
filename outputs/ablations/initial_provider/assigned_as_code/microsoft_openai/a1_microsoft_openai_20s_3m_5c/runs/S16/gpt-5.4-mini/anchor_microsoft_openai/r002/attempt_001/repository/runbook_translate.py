from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def runbook_translate(payload, config=None):
    config = config or {}
    client = TextTranslationClient(endpoint=config['azure_translate_endpoint'], credential=AzureKeyCredential(config['azure_translate_key']))
    result = client.translate(content=[payload.get('notes', '')], to=[payload['target_language']], from_parameter=payload.get('source_language'))
    return {'translation': result[0].translations[0].text}
