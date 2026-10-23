import boto3

def translate_text(text, source_language, target_language):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']