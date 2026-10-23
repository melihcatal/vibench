from typing import Optional, List
from speech_client import PollySpeechClient
from speech_models import Voice, normalize_voice_list


class VoiceSelector:
    """Lists or selects a voice for a target locale using Amazon Polly."""

    def __init__(self):
        self.client = PollySpeechClient()

    def list_voices(self, language_code: Optional[str] = None) -> List[Voice]:
        """List available voices for a target locale."""
        response = self.client.list_voices(language_code)
        return normalize_voice_list(response)

    def select_voice(
        self, language_code: str, gender: Optional[str] = None
    ) -> Optional[Voice]:
        """Select a voice for a target locale and optional gender."""
        voices = self.list_voices(language_code)
        for voice in voices:
            if gender and voice.gender.lower() != gender.lower():
                continue
            return voice
        return None
