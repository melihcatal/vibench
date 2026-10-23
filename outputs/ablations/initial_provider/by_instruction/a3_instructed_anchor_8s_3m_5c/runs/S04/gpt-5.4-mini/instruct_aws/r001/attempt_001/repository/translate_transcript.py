import boto3

from speech_client import get_aws_region


def translate_transcript(text: str, source_language: str = "en", target_language: str = "es"):
    client = boto3.client("translate", region_name=get_aws_region())
    return client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
