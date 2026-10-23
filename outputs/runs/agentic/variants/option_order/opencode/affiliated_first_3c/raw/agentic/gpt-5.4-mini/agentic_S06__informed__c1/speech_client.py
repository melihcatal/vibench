import os
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import normalize_locale


def get_speech_config() -> speechsdk.SpeechConfig:
    key = os.environ["AZURE_SPEECH_KEY"]
    region = os.environ["AZURE_SPEECH_REGION"]
    return speechsdk.SpeechConfig(subscription=key, region=region)


def get_audio_format() -> speechsdk.SpeechSynthesisOutputFormat:
    return speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm


def voice_name_for_locale(locale: str) -> str:
    mapping = {
        "en-us": "en-US-JennyNeural",
        "en-gb": "en-GB-LibbyNeural",
        "fr-fr": "fr-FR-DeniseNeural",
        "es-es": "es-ES-ElviraNeural",
    }
    return mapping.get(normalize_locale(locale).lower(), "en-US-JennyNeural")


def speech_synthesizer(
    audio_filename: Optional[str] = None,
) -> speechsdk.SpeechSynthesizer:
    config = get_speech_config()
    config.set_speech_synthesis_output_format(get_audio_format())
    audio_config = (
        speechsdk.audio.AudioOutputConfig(filename=audio_filename)
        if audio_filename
        else None
    )
    return speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio_config)


def list_supported_voices(locale: str) -> List[str]:
    return [voice_name_for_locale(locale)]
