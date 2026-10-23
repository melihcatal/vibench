import boto3

def translate_query(query, target_language):
    client = boto3.client('translate')
    response = client.translate_text(Text=query, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']