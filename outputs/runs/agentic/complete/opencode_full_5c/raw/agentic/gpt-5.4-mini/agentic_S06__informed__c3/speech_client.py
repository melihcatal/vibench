import os
from typing import Any, Dict, List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import normalize_locale


def speech_config_from_env() -> speechsdk.SpeechConfig:
    key = os.environ["AZURE_SPEECH_KEY"]
    region = os.environ["AZURE_SPEECH_REGION"]
    return speechsdk.SpeechConfig(subscription=key, region=region)


def audio_output_config_to_stream() -> speechsdk.audio.AudioOutputConfig:
    return speechsdk.audio.AudioOutputConfig(use_default_speaker=False)


def list_voices(locale: Optional[str] = None) -> List[Dict[str, Any]]:
    config = speech_config_from_env()
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=config)
    result = speech_synthesizer.get_voices_async(normalize_locale(locale)).get()
    return [
        {
            "name": v.short_name,
            "locale": v.locale,
            "gender": v.gender,
            "style_list": list(getattr(v, "style_list", [])),
        }
        for v in result.voices
    ]


def synthesize_text_payload(text: str, voice: Optional[str] = None) -> bytes:
    config = speech_config_from_env()
    if voice:
        config.speech_synthesis_voice_name = voice
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=None)
    return synthesizer.speak_text_async(text).get().audio_data


def synthesize_ssml_payload(ssml: str, voice: Optional[str] = None) -> bytes:
    config = speech_config_from_env()
    if voice:
        config.speech_synthesis_voice_name = voice
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=None)
    return synthesizer.speak_ssml_async(ssml).get().audio_data
