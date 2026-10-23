import boto3

from speech_client import get_speech_client


def translate_transcript(transcript, target_language, config=None):
    client = get_speech_client(config)
    translate_client = boto3.client('translate', region_name=config.get('region'))
    response = translate_client.translate_text(
        Text=transcript,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language,
    )
    return response['TranslatedText']