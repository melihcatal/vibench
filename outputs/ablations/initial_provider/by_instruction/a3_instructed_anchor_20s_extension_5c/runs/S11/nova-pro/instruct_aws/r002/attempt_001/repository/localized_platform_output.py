import boto3

def translate_output(response, target_language):
    client = boto3.client('translate', region_name='us-west-2')
    text = response['body']['completion']
    result = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result['TranslatedText']