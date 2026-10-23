import boto3

def translate_compliance_note(note_text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=note_text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translatedText