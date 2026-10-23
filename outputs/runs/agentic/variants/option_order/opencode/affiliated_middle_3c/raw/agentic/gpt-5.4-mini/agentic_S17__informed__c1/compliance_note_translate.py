import boto3
from security_client import get_region_name

def compliance_note_translate(text: str, target_language_code: str = 'es') -> str:
    client = boto3.client('translate', region_name=get_region_name())
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language_code)
    return response.get('TranslatedText', '')
