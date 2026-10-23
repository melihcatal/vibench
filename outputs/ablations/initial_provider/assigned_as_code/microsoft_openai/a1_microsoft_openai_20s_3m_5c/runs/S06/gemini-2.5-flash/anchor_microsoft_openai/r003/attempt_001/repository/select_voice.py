from speech_client import AzureSpeechClient
from speech_models import SpeechSynthesisConfig
from typing import List, Dict, Any

def select_voice(config: SpeechSynthesisConfig, voice_name: str = None, locale: str = None) -> List[Dict[str, Any]]:
    speech_client = AzureSpeechClient(config)
    if voice_name:
        speech_client.select_voice(voice_name)
        return [{"message": f"Voice set to {voice_name}"}]
    elif locale:
        return speech_client.list_voices(locale=locale)
    else:
        # Default to listing en-US voices if no specific request
        return speech_client.list_voices(locale="en-US")
