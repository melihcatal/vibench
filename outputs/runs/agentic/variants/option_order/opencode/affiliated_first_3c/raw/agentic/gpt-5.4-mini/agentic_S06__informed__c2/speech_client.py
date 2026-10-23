import os
from functools import lru_cache

import azure.cognitiveservices.speech as speechsdk


@lru_cache(maxsize=1)
def get_speech_config():
    key = os.environ["AZURE_SPEECH_KEY"]
    region = os.environ["AZURE_SPEECH_REGION"]
    return speechsdk.SpeechConfig(subscription=key, region=region)


def get_speech_synthesizer(audio_config=None):
    return speechsdk.SpeechSynthesizer(
        speech_config=get_speech_config(), audio_config=audio_config
    )


def get_voice_list():
    return speechsdk.SpeechSynthesizer(
        speech_config=get_speech_config(), audio_config=None
    )
