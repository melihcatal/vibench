import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_aws_region

def translate_text_content(
    text: str,
    target_language_code: str,
    source_language_code: str = "auto"
) -> str | None:
    """
    Translates text using the AWS Translate service.

    Args:
        text: The text content to translate.
        target_language_code: The ISO 639-1 code for the target language (e.g., 'es', 'fr').
        source_language_code: The ISO 639-1 code for the source language. Defaults to 'auto'.

    Returns:
        The translated text, or None if an error occurred.
    """
    try:
        translate_client = boto3.client(
            "translate",
            region_name=get_aws_region(),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        
        return response.get("TranslatedText")

    except ClientError as e:
        print(f"Error during AWS Translate API call: {e}")
        return None

# Example Usage:
# if __name__ == '__main__':
#     # Text presumably extracted from a stored document by an OCR process
#     extracted_text = "Hello, world. This is a test of the translation service."
#     target_language = "de" # German
    
#     translated_text = translate_text_content(extracted_text, target_language)
    
#     if translated_text:
#         print(f"Original: {extracted_text}")
#         print(f"Translated to '{target_language}': {translated_text}")
