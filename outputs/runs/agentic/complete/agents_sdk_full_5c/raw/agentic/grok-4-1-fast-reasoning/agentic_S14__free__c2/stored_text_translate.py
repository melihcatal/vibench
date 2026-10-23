import boto3
from botocore.exceptions import ClientError

from storage_client import get_aws_credentials

def translate_extracted_text(
    text: str,
    source_language: str = 'en',
    target_language: str = 'es'
) -> str:
    creds = get_aws_credentials()
    translate_client = boto3.client('translate', **creds)
    
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except ClientError as e:
        raise RuntimeError(f"Translation failed: {e}") from e
