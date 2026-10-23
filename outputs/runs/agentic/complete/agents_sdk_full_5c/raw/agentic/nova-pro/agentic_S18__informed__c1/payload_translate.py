import boto3

def payload_translate(text, source_language, target_language):
    translate_client = boto3.client('translate', region_name='us-west-2')
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']