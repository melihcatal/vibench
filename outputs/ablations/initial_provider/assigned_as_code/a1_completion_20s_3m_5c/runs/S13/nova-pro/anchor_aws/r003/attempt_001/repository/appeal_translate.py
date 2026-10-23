import boto3

from safety_client import get_client
from safety_models import normalize_response


def appeal_translate(payload, config=None):
    config = config or {}
    client = get_client(config)
    response = client.translate_text(Text=payload["text"], SourceLanguageCode="en", TargetLanguageCode=config.get("target_language", "es"))
    return {"translated_text": response["TranslatedText"]}