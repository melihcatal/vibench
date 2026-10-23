import boto3


def translate_secret_rotation_runbook_notes(notes, target_language="es"):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=notes, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
