import boto3


def invoice_note_translate(text, target_language="es"):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response.get("TranslatedText")
