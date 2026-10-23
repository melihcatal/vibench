import boto3

from translation_client import get_translate_client
from translation_models import normalize_translation_payload, normalize_translation_response


def unsafe_copy_check(texts, source_language, target_language, config=None):
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
    unsafe_content = [
        check_for_unsafe_content(response) for response in responses
    ]
    return unsafe_content


def check_for_unsafe_content(response):
    # Placeholder for unsafe content check logic
    return False