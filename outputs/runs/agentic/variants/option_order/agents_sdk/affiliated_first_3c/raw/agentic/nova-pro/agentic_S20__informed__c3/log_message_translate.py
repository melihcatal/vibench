import boto3

client = boto3.client('translate', region_name='us-west-2')

def translate_log_message(text, target_language):
    response = client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']