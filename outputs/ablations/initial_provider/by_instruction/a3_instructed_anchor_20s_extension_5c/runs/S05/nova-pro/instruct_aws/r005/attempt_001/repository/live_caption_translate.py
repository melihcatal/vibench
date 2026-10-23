import boto3

def translate_caption(caption, target_language):
    client = boto3.client('translate')
    result = client.translate_text(Text=caption, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result['TranslatedText']