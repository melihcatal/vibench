import boto3

translate = boto3.client('translate')

def stored_text_translate(text, source_language_code, target_language_code):
    response = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response