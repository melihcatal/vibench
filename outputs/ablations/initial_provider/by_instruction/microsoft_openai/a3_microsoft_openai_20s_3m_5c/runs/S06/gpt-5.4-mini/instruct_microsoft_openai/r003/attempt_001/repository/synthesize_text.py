from speech_client import client, speech_model
from speech_models import SpeechRequest, SpeechResult, normalize_text, normalize_voice


def synthesize_text(text: str, voice: str = "alloy", audio_format: str = "mp3") -> bytes:
    req = SpeechRequest(text=normalize_text(text), voice=normalize_voice(voice), format=audio_format)
    response = client().audio.speech.create(model=speech_model(), voice=req.voice, input=req.text, format=req.format)
    return response.read()


def synthesize_text_result(text: str, voice: str = "alloy", audio_format: str = "mp3") -> SpeechResult:
    audio = synthesize_text(text, voice=voice, audio_format=audio_format)
    return SpeechResult(audio=audio, mime_type=f"audio/{audio_format}", voice=normalize_voice(voice), model=speech_model())
