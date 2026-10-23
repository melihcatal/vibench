import boto3


def script_translate(text, source_language, target_language):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']