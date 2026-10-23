import boto3

from observability_client import get_observability_client


def translate_log_message(log_message: str, target_language: str, config=None):
    config = config or {}
    translate_client = boto3.client("translate", region_name=config.get("region"))
    response = translate_client.translate_text(
        Text=log_message,
        SourceLanguageCode="en",
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
