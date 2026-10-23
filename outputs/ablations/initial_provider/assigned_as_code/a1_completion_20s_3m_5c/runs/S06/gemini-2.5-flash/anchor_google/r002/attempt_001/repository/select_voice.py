from speech_client import SpeechClient
from speech_models import VoiceInfo

def select_voice(language_code: str):
    client = SpeechClient().get_client()
    response = client.list_voices(language_code=language_code)
    voices = [VoiceInfo.from_texttospeech_voice(v) for v in response.voices]
    return {"voices": [v.__dict__ for v in voices]}
