import boto3

from storage_models import normalize_text


def stored_text_translate(text, source_language="auto", target_language="en"):
    client = boto3.client("translate")
    return client.translate_text(
        Text=normalize_text(text),
        SourceLanguageCode=source_language if source_language != "auto" else "auto",
        TargetLanguageCode=target_language,
    )
