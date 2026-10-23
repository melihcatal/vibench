import boto3

def appeal_translate(text, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']
