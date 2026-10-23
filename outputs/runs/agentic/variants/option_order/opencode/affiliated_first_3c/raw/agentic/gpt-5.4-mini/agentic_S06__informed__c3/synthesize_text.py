import azure.cognitiveservices.speech as speechsdk

from speech_client import require_config
from speech_models import SynthesisRequest, SynthesisResult, normalize_text


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> SynthesisResult:
    config = require_config()
    request = SynthesisRequest(text=normalize_text(text), voice=voice or config.voice_name, locale=locale or config.language)
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    if request.output_format:
        speech_config.set_speech_synthesis_output_format(getattr(speechsdk.SpeechSynthesisOutputFormat, request.output_format))
    if request.voice:
        speech_config.speech_synthesis_voice_name = request.voice
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(request.text).get()
    audio = result.audio_data if result and result.audio_data else b""
    return SynthesisResult(audio=audio, content_type="audio/wav", metadata={"reason": getattr(result, "reason", None)})
