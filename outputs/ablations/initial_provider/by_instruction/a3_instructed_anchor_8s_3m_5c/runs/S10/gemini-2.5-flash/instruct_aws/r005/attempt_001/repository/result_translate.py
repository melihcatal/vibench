import boto3
import os

def translate_text(text: str, source_language: str, target_language: str) -> str:
    """
    Translates the given text using AWS Translate.
    """
    translate_client = boto3.client(
        service_name='translate',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response['TranslatedText']
