from database_client import get_boto3_client
from botocore.exceptions import ClientError

def translate_record_field(text: str, target_language: str, source_language: str = "auto") -> str:
    """
    Translates a text field in a record using Amazon Translate.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es').
        source_language: The ISO 639-1 code for the source language (e.g., 'en').
                         Defaults to 'auto' for automatic detection.

    Returns:
        The translated text, or the original text if an error occurs.
    """
    translate_client = get_boto3_client('translate')

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response.get('TranslatedText', text)
    except ClientError as e:
        print(f"An error occurred with AWS Translate: {e}")
        return text
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return text
