from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_alt_text(text, target_language, config=None):
    config = config or {}
    with TextTranslationClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.translate([text], target_language)
    return result[0].translation