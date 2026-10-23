import boto3


def invoice_note_translate(text, target_language_code="es"):
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code)
    return response.get("TranslatedText")
