import boto3

def translate_payload(payload, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=payload, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.translatedText