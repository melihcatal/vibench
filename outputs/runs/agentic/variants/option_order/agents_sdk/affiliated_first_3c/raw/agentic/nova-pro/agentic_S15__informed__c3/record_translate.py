import boto3

translate = boto3.client('translate')

def translate_record(text, source_language_code, target_language_code):
    response = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response['TranslatedText']