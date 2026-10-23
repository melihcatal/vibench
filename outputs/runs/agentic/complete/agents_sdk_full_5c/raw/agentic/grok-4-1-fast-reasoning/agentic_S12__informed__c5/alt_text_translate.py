import boto3
from typing import Optional

def alt_text_translate(alt_text: str, target_language: str = 'es', source_language: Optional[str] = None) -> str:
    client = boto3.client('translate')
    kwargs = {
        'Text': alt_text,
        'TargetLanguageCode': target_language
    }
    if source_language:
        kwargs['SourceLanguageCode'] = source_language
    result = client.translate_text(**kwargs)
    return result['TranslatedText']