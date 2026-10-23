import boto3
from security_models import normalize_text


def compliance_note_translate(note: str, target_language_code: str = 'es'):
    translate = boto3.client('translate')
    normalized = normalize_text(note)
    response = translate.translate_text(Text=normalized, SourceLanguageCode='en', TargetLanguageCode=target_language_code)
    return {'provider': 'Amazon Translate', 'translated_text': response['TranslatedText'], 'target_language_code': target_language_code}
