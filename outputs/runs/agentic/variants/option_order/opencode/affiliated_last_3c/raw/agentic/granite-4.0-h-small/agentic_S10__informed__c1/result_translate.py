# Translate generated model output using Amazon Translate via Boto3
import boto3


def translate_text(text: str, target_lang: str = "es") -> str:
    """Translate text into a target language using Amazon Translate.

    Args:
        text: Source text to translate.
        target_lang: ISO language code (default Spanish).

    Returns:
        Translated text.
    """
    client = boto3.client(service_name="translate", region_name="us-east-1")
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_lang
    )
    return response.get("TranslatedText", "")
