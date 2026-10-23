import boto3

def translate_markup(html_content: str, source_language: str, target_language: str) -> str:
    """
    Translates HTML or markup while preserving tags using AWS Translate.
    """
    client = boto3.client('translate')
    response = client.translate_text(
        Text=html_content,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        TextType='HTML'
    )
    return response['TranslatedText']
