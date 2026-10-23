import boto3

from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse


def translate_markup(markup, source_language, target_language, config=None):
    client = get_translate_client(config)
    request = TranslationRequest(text=markup, source_language=source_language, target_language=target_language).to_dict()
    response = client.translate_text(**request)
    return TranslationResponse.from_dict(response).to_dict()