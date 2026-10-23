import boto3
import os

def script_translate(text: str, source_language_code: str, target_language_code: str) -> str:
    """
    Translates narration scripts using Amazon Translate.

    Args:
        text: The text to translate.
        source_language_code: The language code of the input text (e.g., "en").
        target_language_code: The language code to translate the text to (e.g., "es").

    Returns:
        The translated text.
    """
    translate_client = boto3.client(
        'translate',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response.get('TranslatedText', text)
