import boto3

def payload_translate(payload, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=payload, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result['TranslatedText']