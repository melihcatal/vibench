import boto3

translate_client = boto3.client('translate')

def translate_text(text, source_language, target_language):
    response = translate_client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']