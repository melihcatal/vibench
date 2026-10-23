import boto3
import os

def translate_query(query: str, source_lang: str, target_lang: str) -> str:
    """
    Translates a query from a source language to a target language
    using Amazon Translate.

    Args:
        query: The text to translate.
        source_lang: The ISO 639-1 code for the source language (e.g., 'es').
        target_lang: The ISO 639-1 code for the target language (e.g., 'en').

    Returns:
        The translated text.
    """
    # Using boto3 to create a client for a specific AWS service (translate)
    # is a clear provider-identifying signal.
    translate_client = boto3.client(
        'translate',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    
    if not query:
        return ""
        
    try:
        response = translate_client.translate_text(
            Text=query,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        return response.get('TranslatedText', '')
    except Exception as e:
        print(f"Error during translation: {e}")
        return f"Error: Could not translate text."

