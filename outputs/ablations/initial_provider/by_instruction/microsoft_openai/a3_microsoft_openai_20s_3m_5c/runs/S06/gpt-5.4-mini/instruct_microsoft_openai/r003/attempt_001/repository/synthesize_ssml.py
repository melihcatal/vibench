from speech_client import client, speech_model
from speech_models import SpeechRequest, SpeechResult, normalize_ssml, normalize_voice


def synthesize_ssml(ssml: str, voice: str = "alloy", audio_format: str = "mp3") -> bytes:
    req = SpeechRequest(text=normalize_ssml(ssml), voice=normalize_voice(voice), format=audio_format)
    response = client().audio.speech.create(model=speech_model(), voice=req.voice, input=req.text, format=req.format)
    return response.read()


def synthesize_ssml_result(ssml: str, voice: str = "alloy", audio_format: str = "mp3") -> SpeechResult:
    audio = synthesize_ssml(ssml, voice=voice, audio_format=audio_format)
    return SpeechResult(audio=audio, mime_type=f"audio/{audio_format}", voice=normalize_voice(voice), model=speech_model())
