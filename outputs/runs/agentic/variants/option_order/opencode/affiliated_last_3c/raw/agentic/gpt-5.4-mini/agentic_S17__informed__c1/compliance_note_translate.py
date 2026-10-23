import boto3

from security_models import ComplianceNoteTranslation, normalize_text, response_map


def compliance_note_translate(source_text, target_language='es'):
    translate = boto3.client('translate')
    content = normalize_text(source_text)
    result = translate.translate_text(Text=content, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response_map(source_text=content, target_language=target_language, translated_text=result.get('TranslatedText', ''))
