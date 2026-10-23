import os
from typing import Dict

import boto3


class LocalizedAudioPreview:
    def __init__(self, region_name: str | None = None):
        self.client = boto3.client("polly", region_name=region_name or os.getenv("AWS_REGION"))

    def generate(self, text: str, language_code: str) -> Dict[str, bytes]:
        response = self.client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna", LanguageCode=language_code)
        return {"audio": response["AudioStream"].read(), "provider": "amazon_polly"}


def localized_audio_preview(text: str, language_code: str) -> Dict[str, bytes]:
    return LocalizedAudioPreview().generate(text, language_code)
