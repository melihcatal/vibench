import boto3

from speech_client import get_translate_client


def translate_transcript(transcript, target_language_code, config=None):
    config = config or {}
    client = get_translate_client(config)
    response = client.translate_text(
        Text=transcript,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language_code,
    )
    return response["TranslatedText"]