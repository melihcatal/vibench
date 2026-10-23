import boto3

def translate_text(text: str, source_language: str, target_language: str) -> str:
    """
    Translates a single text string between languages using AWS Translate.
    """
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']
