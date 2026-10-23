import boto3

translate_client = boto3.client('translate')

def translate_script(text, source_language_code, target_language_code):
    result = translate_client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result['TranslatedText']