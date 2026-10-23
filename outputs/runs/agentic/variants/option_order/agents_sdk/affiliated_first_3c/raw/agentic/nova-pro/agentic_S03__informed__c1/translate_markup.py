import boto3

def translate_markup(markup, source_language, target_language):
    client = boto3.client('translate')
    result = client.translate_text(Text=markup, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result['TranslatedText']