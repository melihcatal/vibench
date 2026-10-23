import boto3
from typing import Optional

def translate_dashboard_note(
    text: str,
    target_language_code: str = 'fr',
    source_language_code: Optional[str] = None,
    region: str = 'us-east-1'
) -> str:
    client = boto3.client('translate', region_name=region)
    result = client.translate_text(
        Text=text,
        TargetLanguageCode=target_language_code,
        SourceLanguageCode=source_language_code
    )
    return result['TranslatedText']
