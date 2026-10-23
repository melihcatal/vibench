import boto3


def translate_runbook_notes(notes, target_language):
    client = boto3.client("translate")
    translate_response = client.translate_text(
        Text=notes, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return translate_response["TranslatedText"]
