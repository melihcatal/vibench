import boto3

def translate_platform_output(output, target_language='fr'):
    client = boto3.client('translate', region_name='us-west-2')
    response = client.translate_text(
        Text=output,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']