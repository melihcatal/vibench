import boto3


def compliance_note_translate(text, target_language):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
