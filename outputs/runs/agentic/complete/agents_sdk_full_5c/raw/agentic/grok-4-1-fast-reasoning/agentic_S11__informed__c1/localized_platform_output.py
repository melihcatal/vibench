import boto3

def localize_platform_output(text: str, source_lang: str = 'en', target_lang: str = 'fr') -> str:
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']
