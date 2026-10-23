from google.cloud import texttospeech

from speech_client import build_synthesis_input, get_client, get_voice_name
from speech_models import SpeechRequest, SpeechResponse


def synthesize_ssml(ssml: str, locale: str = "en-US", voice: str = None, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    request = SpeechRequest(text=ssml, locale=locale, voice=voice, ssml=True, speaking_rate=speaking_rate, pitch=pitch)
    client = get_client()
    voice_name = get_voice_name(request.locale, request.voice)
    voice_params = texttospeech.VoiceSelectionParams(language_code=request.locale, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=speaking_rate, pitch=pitch)
    response = client.synthesize_speech(input=build_synthesis_input(request), voice=voice_params, audio_config=audio_config)
    return SpeechResponse(audio=response.audio_content, voice=voice_name, locale=request.locale).audio
