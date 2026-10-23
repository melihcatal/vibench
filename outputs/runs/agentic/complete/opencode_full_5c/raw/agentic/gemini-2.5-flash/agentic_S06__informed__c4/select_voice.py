from speech_client import TextToSpeechClient
from typing import List, Dict, Any, Optional


def select_voice(language_code: Optional[str] = None) -> List[Dict[str, Any]]:
    client = TextToSpeechClient()
    voices = client.list_voices(language_code=language_code)
    return voices
