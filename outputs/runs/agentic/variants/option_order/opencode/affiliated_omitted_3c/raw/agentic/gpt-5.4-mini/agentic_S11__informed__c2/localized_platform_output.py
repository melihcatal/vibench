import boto3


def localized_platform_output(text: str, target_language: str = "es"):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return {
        "translated_text": response.get("TranslatedText", ""),
        "provider": "Amazon Translate",
    }
