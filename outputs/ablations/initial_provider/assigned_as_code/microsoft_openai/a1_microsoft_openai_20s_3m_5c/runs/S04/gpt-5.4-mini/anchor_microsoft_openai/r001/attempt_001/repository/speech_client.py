import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    region: str
    api_key: str
    model: str = 'whisper-1'


def load_speech_config(config=None):
    config = config or {}
    return SpeechConfig(
        region=config.get('region') or os.environ['AZURE_SPEECH_REGION'],
        api_key=config.get('api_key') or os.environ['AZURE_SPEECH_KEY'],
        model=config.get('model') or 'whisper-1',
    )


def speech_endpoint(region, path):
    return f'https://{region}.api.cognitive.microsoft.com/{path}'
