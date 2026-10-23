import boto3


def compliance_note_translate(text):
    client = boto3.client("translate", region_name="us-west-2")
    response = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
