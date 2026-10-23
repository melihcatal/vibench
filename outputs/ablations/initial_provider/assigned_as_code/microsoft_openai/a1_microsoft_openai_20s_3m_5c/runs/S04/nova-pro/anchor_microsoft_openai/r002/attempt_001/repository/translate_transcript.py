import boto3

translate = boto3.client('translate')

def translate_transcript(text, source_language_code='en', target_language_code='es'):
    response = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response['TranslatedText']