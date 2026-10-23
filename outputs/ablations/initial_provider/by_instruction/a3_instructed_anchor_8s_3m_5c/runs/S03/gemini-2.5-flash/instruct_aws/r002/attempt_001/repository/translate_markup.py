import boto3

def translate_markup(markup_text: str, source_language: str, target_language: str) -> str:
    """
    Translates HTML or markup while preserving tags using AWS Translate.
    """
    client = boto3.client("translate")
    response = client.translate_text(
        Text=markup_text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        Settings={'Formality': 'FORMAL', 'Profanity' : 'NO'},
        TextType="HTML"
    )
    return response["TranslatedText"]
