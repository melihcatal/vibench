import boto3

from messaging_client import get_client


def translate_payload(payload, config=None):
    config = config or {}
    client = get_client("translate", config)
    response = client.translate_text(Text=payload, SourceLanguageCode="en", TargetLanguageCode="es")
    return response["TranslatedText"]