import boto3


def runbook_translate(text):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
