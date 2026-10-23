from speech_client import speech_synthesizer, voice_name_for_locale
from speech_models import SpeechRequest, SpeechResponse, normalize_text


def synthesize_ssml(
    ssml: str,
    locale: str = "en-US",
    voice: str = None,
    rate: str = "0%",
    pitch: str = "0%",
) -> SpeechResponse:
    req = SpeechRequest(text=ssml, locale=locale, voice=voice)
    synth = speech_synthesizer()
    voice_name = req.voice or voice_name_for_locale(req.locale)
    synth.speech_synthesis_voice_name = voice_name
    body = normalize_text(req.text)
    ssml_payload = f"<speak version='1.0' xml:lang='{req.locale}'><voice name='{voice_name}'><prosody rate='{rate}' pitch='{pitch}'>{body}</prosody></voice></speak>"
    result = synth.speak_ssml_async(ssml_payload).get()
    return SpeechResponse(
        audio=bytes(result.audio_data), content_type="audio/wav", voice=voice_name
    )
