from google.cloud import texttospeech

from speech_client import build_synthesis_input, get_client, get_voice_name
from speech_models import SpeechRequest, SpeechResponse


def synthesize_text(text: str, locale: str = "en-US", voice: str = None) -> bytes:
    request = SpeechRequest(text=text, locale=locale, voice=voice, ssml=False)
    client = get_client()
    voice_name = get_voice_name(request.locale, request.voice)
    voice_params = texttospeech.VoiceSelectionParams(language_code=request.locale, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(input=build_synthesis_input(request), voice=voice_params, audio_config=audio_config)
    return SpeechResponse(audio=response.audio_content, voice=voice_name, locale=request.locale).audio
