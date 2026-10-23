import boto3


def runbook_translate(
    text: str, source_language: str = "en", target_language: str = "es"
) -> str:
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
