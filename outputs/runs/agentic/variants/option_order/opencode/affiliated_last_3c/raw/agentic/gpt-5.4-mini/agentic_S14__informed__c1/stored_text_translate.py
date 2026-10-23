import boto3


def translate_text(text: str, source_language: str, target_language: str) -> str:
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
