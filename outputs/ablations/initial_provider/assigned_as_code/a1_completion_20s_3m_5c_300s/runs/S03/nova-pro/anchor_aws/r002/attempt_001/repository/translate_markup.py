import boto3

from translation_client import get_translate_client
from translation_models import normalize_translation_payload, normalize_translation_response


def translate_markup(markup, source_language, target_language, config=None):
    client = get_translate_client(config)
    payload = normalize_translation_payload(
        text=markup,
        source_language=source_language,
        target_language=target_language,
    )
    response = client.translate_text(**payload)
    translated_text = response["TranslatedText"]
    return normalize_translation_response(response)