import boto3
from typing import Optional

def translate_dashboard_note(
    note: str,
    target_language: str = 'fr',
    source_language: Optional[str] = None
) -> str:
    """Translate metric or dashboard notes for another locale using Amazon Translate."""
    client = boto3.client('translate')
    kwargs = {
        'Text': note,
        'SourceLanguageCode': source_language or 'auto',
        'TargetLanguageCode': target_language
    }
    result = client.translate_text(**kwargs)
    return result['TranslatedText']