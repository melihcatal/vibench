import boto3


def translate_secret_rotation_runbook_notes(notes, target_language):
    client = boto3.client("translate")
    result = client.translate_text(
        Text=notes, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return result["TranslatedText"]
