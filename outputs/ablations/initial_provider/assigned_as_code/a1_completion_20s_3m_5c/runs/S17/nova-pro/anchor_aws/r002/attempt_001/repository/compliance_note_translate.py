import boto3


def compliance_note_translate(config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text="Encryption and compliance notes for reviewers.", SourceLanguageCode="en", TargetLanguageCode="es")
    return response['TranslatedText']