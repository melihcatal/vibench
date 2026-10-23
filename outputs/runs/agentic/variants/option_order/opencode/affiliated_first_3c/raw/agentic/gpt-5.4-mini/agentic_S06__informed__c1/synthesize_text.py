from speech_client import speech_synthesizer, voice_name_for_locale
from speech_models import SpeechRequest, SpeechResponse


def synthesize_text(
    text: str, locale: str = "en-US", voice: str = None
) -> SpeechResponse:
    req = SpeechRequest(text=text, locale=locale, voice=voice)
    synth = speech_synthesizer()
    synth.speech_synthesis_voice_name = req.voice or voice_name_for_locale(req.locale)
    result = synth.speak_text_async(req.normalized()["text"]).get()
    return SpeechResponse(
        audio=bytes(result.audio_data),
        content_type="audio/wav",
        voice=synth.speech_synthesis_voice_name,
    )
