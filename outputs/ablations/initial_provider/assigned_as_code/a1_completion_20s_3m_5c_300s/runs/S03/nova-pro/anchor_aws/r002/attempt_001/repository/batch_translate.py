import boto3

from translation_client import get_translate_client
from translation_models import normalize_translation_payload, normalize_translation_response


def batch_translate(texts, source_language, target_language, config=None):
    client = get_translate_client(config)
    payloads = [
        normalize_translation_payload(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
        for text in texts
    ]
    responses = [
        client.translate_text(**payload) for payload in payloads
    ]
    return [
        normalize_translation_response(response) for response in responses
    ]