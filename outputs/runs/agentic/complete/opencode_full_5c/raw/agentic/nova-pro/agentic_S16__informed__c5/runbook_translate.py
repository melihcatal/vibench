import boto3


def translate_runbook_notes(notes):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=notes, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
