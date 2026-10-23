import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_synthesizer
from speech_models import (
    SpeechRequest,
    SpeechResponse,
    build_ssml,
    normalize_locale,
    normalize_voice,
)


def synthesize_ssml(request: SpeechRequest) -> SpeechResponse:
    synthesizer = get_speech_synthesizer()
    voice = normalize_voice(request.voice, request.locale)
    ssml = request.ssml or build_ssml(
        request.text or "",
        voice or "en-US-AriaNeural",
        normalize_locale(request.locale),
        request.prosody_rate,
        request.prosody_pitch,
    )
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(str(result.reason))
    return SpeechResponse(
        audio=result.audio_data, voice=voice, format=request.output_format
    )
