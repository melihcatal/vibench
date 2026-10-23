import boto3


def compliance_note_translate(text):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return response["TranslatedText"]
