import azure.cognitiveservices.speech as speechsdk

from speech_client import ensure_azure_config
from speech_models import normalize_text


def synthesize_text(text: str, voice: str | None = None) -> bytes:
    config = ensure_azure_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    speech_config.speech_synthesis_voice_name = (
        voice or config.voice or "en-US-AriaNeural"
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    result = synthesizer.speak_text_async(normalize_text(text)).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(str(result.reason))
    return result.audio_data
