import boto3


def translate_secret_rotation_runbook_notes(notes):
    client = boto3.client("translate")
    translate_text_response = client.translate_text(
        Text=notes, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return translate_text_response["TranslatedText"]
