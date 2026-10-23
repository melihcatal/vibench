from boto3 import client


def compliance_note_translate(text, target_language):
    translate_client = client("translate")
    response = translate_client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
