import boto3

from speech_models import build_translation_request


def translate_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    request = build_translation_request(
        payload["text"],
        payload["target_language"],
        payload.get("source_language"),
    )
    response = client.translate_text(**{k: v for k, v in request.items() if v is not None})
    return {
        "translated_text": response["TranslatedText"],
        "source_language": response.get("SourceLanguageCode"),
        "target_language": response.get("TargetLanguageCode"),
    }
