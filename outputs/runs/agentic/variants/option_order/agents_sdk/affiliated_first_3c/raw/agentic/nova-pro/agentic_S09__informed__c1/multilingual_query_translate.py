import boto3

def translate_query(text, target_language):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return response['TranslatedText']