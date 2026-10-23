import boto3

from security_models import normalize_text


def compliance_note_translate(text: str, target_language: str):
    client = boto3.client("translate")
    return client.translate_text(
        Text=normalize_text(text),
        SourceLanguageCode="en",
        TargetLanguageCode=normalize_text(target_language),
    )
