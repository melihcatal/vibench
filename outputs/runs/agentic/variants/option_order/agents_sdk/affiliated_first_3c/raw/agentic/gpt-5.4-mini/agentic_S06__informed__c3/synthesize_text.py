from azure.cognitiveservices import speech as speechsdk

from speech_client import create_synthesizer, load_speech_config, normalize_voice_name
from speech_models import TTSRequest, TTSResponse, normalize_text


def synthesize_text(text: str, locale: str = "en-US", voice: str = None) -> TTSResponse:
    request = TTSRequest(text=normalize_text(text), locale=locale, voice=voice)
    cfg = load_speech_config()
    selected_voice = normalize_voice_name(request.locale, request.voice or cfg.voice)
    synthesizer = create_synthesizer()
    if selected_voice:
        synthesizer.speech_synthesis_voice_name = selected_voice
    result = synthesizer.speak_text_async(request.text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure Speech TTS failed: {result.reason}")
    return TTSResponse(audio_bytes=result.audio_data, content_type="audio/wav", voice=selected_voice)
