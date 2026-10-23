from typing import List, Optional
from speech_client import PollySpeechClient
from speech_models import Voice, normalize_voice_list


def select_voice(language_code: Optional[str] = None) -> List[Voice]:
    """
    Lists or selects a voice for a target locale using Amazon Polly.
    """
    client = PollySpeechClient()
    voices_data = client.list_voices(language_code)
    return normalize_voice_list(voices_data)
