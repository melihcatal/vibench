import boto3


def log_message_translate(text, source_language="en", target_language="es"):
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response.get("TranslatedText")
