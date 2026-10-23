import json
from google.cloud import translate_v3 as translate
from messaging_models import normalize_payload_text


def translate_payload(payload, target_language='es'):
    client = translate.TranslationServiceClient()
    text = normalize_payload_text(payload)
    parent = f"projects/{__import__('os').environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    response = client.translate_text(request={'parent': parent, 'contents': [text], 'mime_type': 'text/plain', 'target_language_code': target_language})
    return json.dumps({'source_text': text, 'translated_text': response.translations[0].translated_text, 'target_language': target_language}, sort_keys=True)
