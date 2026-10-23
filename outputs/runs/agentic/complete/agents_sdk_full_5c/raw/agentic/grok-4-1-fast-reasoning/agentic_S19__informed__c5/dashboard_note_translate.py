import boto3

def translate_dashboard_note(
    text: str,
    source_language: str = 'en',
    target_language: str = 'fr'
) -> str:
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']
