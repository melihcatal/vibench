import boto3
from typing import Dict, Any

def translate_dictionary_values(d: Dict[str, Any], source_lang: str, target_lang: str) -> Dict[str, Any]:
    """
    Translates dictionary values while preserving keys using AWS Translate.
    """
    client = boto3.client('translate', region_name='us-east-1')
    new_d = {}
    for k, v in d.items():
        if isinstance(v, str):
            result = client.translate_text(Text=v, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
            new_d[k] = result['TranslatedText']
        else:
            new_d[k] = v  # non-str unchanged
    return new_d