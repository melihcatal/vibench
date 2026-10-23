import boto3

def translate_text(text: str, source_language: str, target_language: str) -> str:
    """
    Translates the given text using AWS Translate.
    """
    translate = boto3.client(
        service_name="translate",
        region_name="us-east-1"
    )

    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response.get("TranslatedText")

