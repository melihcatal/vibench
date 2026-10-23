import boto3

def translate_invoice_note(note, source_language, target_language):
    translate = boto3.client('translate', region_name='us-east-1')
    result = translate.translate_text(Text=note, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translatedText