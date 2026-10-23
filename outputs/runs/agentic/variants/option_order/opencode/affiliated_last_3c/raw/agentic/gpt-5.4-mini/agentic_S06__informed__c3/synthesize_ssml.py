import azure.cognitiveservices.speech as speechsdk

from speech_client import ensure_azure_config
from speech_models import wrap_ssml


def synthesize_ssml(
    text: str, voice: str, locale: str = "en-US", rate: str = "0%", pitch: str = "0%"
) -> bytes:
    config = ensure_azure_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    ssml = wrap_ssml(text, voice=voice, locale=locale, rate=rate, pitch=pitch)
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(str(result.reason))
    return result.audio_data
