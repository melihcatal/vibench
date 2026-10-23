import boto3

from speech_client import load_config


def translate_transcript(text: str, source_language: str = "en", target_language: str = "es") -> str:
    config = load_config()
    client = boto3.client(
        "translate",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response.get("TranslatedText", "")
