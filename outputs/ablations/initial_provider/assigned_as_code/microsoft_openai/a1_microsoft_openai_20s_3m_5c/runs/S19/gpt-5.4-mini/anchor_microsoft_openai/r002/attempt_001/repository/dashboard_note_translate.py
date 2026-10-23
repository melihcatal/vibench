from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def dashboard_note_translate(payload, config=None):
    endpoint = (config or {}).get('endpoint') or payload.get('endpoint')
    key = (config or {}).get('api_key') or payload.get('api_key')
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=(config or {}).get('region') or payload.get('region'))
    response = client.translate(content=[payload['text']], to=[payload['target_locale']])
    return {'translated_text': response[0].translations[0].text}
