import boto3


def payload_translate(text, source_language="auto", target_language="en"):
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response.get("TranslatedText", text)
