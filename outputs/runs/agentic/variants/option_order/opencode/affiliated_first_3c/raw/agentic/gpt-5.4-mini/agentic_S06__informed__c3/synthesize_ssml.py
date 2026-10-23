import azure.cognitiveservices.speech as speechsdk

from speech_client import require_config
from speech_models import SynthesisRequest, SynthesisResult, normalize_ssml


def synthesize_ssml(ssml: str, voice: str, rate: str | None = None, pitch: str | None = None) -> SynthesisResult:
    config = require_config()
    request = SynthesisRequest(text="", voice=voice, ssml=normalize_ssml(ssml), locale=config.language)
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    if request.voice:
        speech_config.speech_synthesis_voice_name = request.voice
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    payload = request.ssml or ""
    if rate or pitch:
        payload = payload.replace("<prosody", f'<prosody rate="{rate or "medium"}" pitch="{pitch or "default"}"', 1)
    result = synthesizer.speak_ssml_async(payload).get()
    audio = result.audio_data if result and result.audio_data else b""
    return SynthesisResult(audio=audio, content_type="audio/wav", metadata={"reason": getattr(result, "reason", None)})
