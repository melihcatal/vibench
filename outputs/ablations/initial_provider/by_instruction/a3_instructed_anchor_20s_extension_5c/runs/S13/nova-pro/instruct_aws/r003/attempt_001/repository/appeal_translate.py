import boto3

def translate_appeal_text(text, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, TargetLanguageCode=target_language)
    return response.translatedText
