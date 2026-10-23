import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_synthesizer
from speech_models import (
    SpeechRequest,
    SpeechResponse,
    normalize_locale,
    normalize_voice,
)


def synthesize_text(request: SpeechRequest) -> SpeechResponse:
    synthesizer = get_speech_synthesizer()
    voice = normalize_voice(request.voice, request.locale)
    if voice:
        synthesizer.speech_config.speech_synthesis_voice_name = voice
    synthesizer.speech_config.speech_synthesis_language = normalize_locale(
        request.locale
    )
    result = synthesizer.speak_text_async(request.text or "").get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(str(result.reason))
    return SpeechResponse(
        audio=result.audio_data, voice=voice, format=request.output_format
    )
