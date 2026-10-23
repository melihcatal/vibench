import boto3
from translation_client import get_translate_client
from translation_models import normalize_payload, parse_translation_response


def translate_markup(payload, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))

    normalized_payload = normalize_payload(payload)

    response = client.translate_text(
        Text=normalized_payload["Text"],
        SourceLanguageCode=normalized_payload["SourceLanguageCode"],
        TargetLanguageCode=normalized_payload["TargetLanguageCode"],
        TextType="HTML",
    )

    return parse_translation_response(response, normalized_payload)
