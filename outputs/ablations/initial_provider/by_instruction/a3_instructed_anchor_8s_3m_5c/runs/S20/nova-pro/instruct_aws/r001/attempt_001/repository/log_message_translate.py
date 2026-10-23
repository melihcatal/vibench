import boto3

def translate_log_message(log_message, target_language):
    translate = boto3.client('translate', region_name='us-east-1')
    response = translate.translate_text(Text=log_message, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']