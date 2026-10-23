import boto3

translate_client = boto3.client('translate')

def translate_transcript(text, target_language):
    response = translate_client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']