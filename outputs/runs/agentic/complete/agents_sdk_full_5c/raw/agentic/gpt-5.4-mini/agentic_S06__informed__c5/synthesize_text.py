from __future__ import annotations

from speech_client import SpeechClientFactory
from speech_models import TextToSpeechRequest, TextToSpeechResponse


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> TextToSpeechResponse:
    request = TextToSpeechRequest(text=text, voice=voice, locale=locale)
    cfg = SpeechClientFactory.from_env()
    cfg.voice = SpeechClientFactory.request_to_voice(request)
    synthesizer = SpeechClientFactory.build_synthesizer(cfg)
    result = synthesizer.speak_text_async(request.normalized_text()).get()
    audio = bytes(result.audio_data) if getattr(result, "audio_data", None) is not None else b""
    return TextToSpeechResponse(audio_bytes=audio, metadata={"reason": getattr(result, "reason", None)})
