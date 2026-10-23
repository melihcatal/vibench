import boto3

from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse


def batch_translate(texts, source_language, target_language, config=None):
    client = get_translate_client(config)
    requests = [
        TranslationRequest(text=text, source_language=source_language, target_language=target_language).to_dict()
        for text in texts
    ]
    responses = client.batch_translate_text(Requests=requests)
    return [
        TranslationResponse.from_dict(response).to_dict()
        for response in responses['TranslatedTexts']
    ]