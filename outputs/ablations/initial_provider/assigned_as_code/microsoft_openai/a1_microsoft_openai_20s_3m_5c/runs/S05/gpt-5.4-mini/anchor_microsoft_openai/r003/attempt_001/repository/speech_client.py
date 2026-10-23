import os
from dataclasses import dataclass

import azure.cognitiveservices.speech as speechsdk


@dataclass
class SpeechClientConfig:
    api_key: str
    region: str


def load_speech_config(config=None):
    data = dict(config or {})
    api_key = data.get('api_key') or os.getenv('AZURE_SPEECH_KEY')
    region = data.get('region') or os.getenv('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('Azure Speech configuration requires api_key and region')
    return SpeechClientConfig(api_key=api_key, region=region)


def build_speech_config(config=None):
    speech_config = load_speech_config(config)
    return speechsdk.SpeechConfig(subscription=speech_config.api_key, region=speech_config.region)


def build_push_stream(sample_rate_hz):
    return speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat(samples_per_second=sample_rate_hz, bits_per_sample=16, channels=1))
