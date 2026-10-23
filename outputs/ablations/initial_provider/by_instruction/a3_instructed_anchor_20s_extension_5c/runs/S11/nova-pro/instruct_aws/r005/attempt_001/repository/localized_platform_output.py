import boto3

def translate_output(output, target_language='es'):
    client = boto3.client('translate', region_name='us-west-2')
    response = client.translate_text(
        Text=output,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']