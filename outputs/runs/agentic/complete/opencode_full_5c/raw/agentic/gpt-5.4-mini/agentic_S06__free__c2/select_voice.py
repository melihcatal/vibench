from typing import List, Optional

from azure.cognitiveservices.speech import SpeechSynthesizer

from speech_client import build_speech_config, target_locale


def select_voice(
    locale: Optional[str] = None, voices: Optional[List[str]] = None
) -> str:
    if voices:
        return voices[0]
    config = build_speech_config()
    synth = SpeechSynthesizer(speech_config=config, audio_config=None)
    if locale:
        locale = target_locale(locale)
    voices_result = (
        synth.get_voices_async(locale).get()
        if locale
        else synth.get_voices_async().get()
    )
    if not voices_result.voices:
        raise RuntimeError("No voices available")
    return voices_result.voices[0].short_name
