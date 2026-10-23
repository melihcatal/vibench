import boto3
from translation_client import get_translate_client
from translation_models import normalize_batch_payload, parse_batch_translation_response


def batch_translate(payloads, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))

    normalized_payloads = normalize_batch_payload(payloads)
    translated_responses = []

    for item in normalized_payloads:
        response = client.translate_text(
            Text=item["Text"],
            SourceLanguageCode=item["SourceLanguageCode"],
            TargetLanguageCode=item["TargetLanguageCode"],
        )
        translated_responses.append(response)

    return parse_batch_translation_response(translated_responses, normalized_payloads)
