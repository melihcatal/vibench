from speech_client import get_tts_client
from speech_models import ListVoicesResponse, VoiceConfig
from google.cloud import texttospeech

def select_voice(language_code: str, name: str = None) -> ListVoicesResponse:
    client = get_tts_client()
    
    # The client can also be used to list the client's supported voices.
    voices = client.list_voices(language_code=language_code).voices

    if name:
        filtered_voices = [voice for voice in voices if voice.name == name]
        return ListVoicesResponse(voices=filtered_voices)
    
    return ListVoicesResponse(voices=voices)
