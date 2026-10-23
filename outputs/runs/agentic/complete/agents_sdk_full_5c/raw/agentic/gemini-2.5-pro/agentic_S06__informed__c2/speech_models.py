from dataclasses import dataclass
from google.cloud.texttospeech import Voice
from typing import List

@dataclass
class SpeechVoice:
    name: str
    language_code: str
    gender: str

    @staticmethod
    def from_api_voice(voice: Voice) -> "SpeechVoice":
        """Creates a SpeechVoice from the Google Cloud TTS API Voice object."""
        return SpeechVoice(
            name=voice.name,
            language_code=voice.language_codes[0],
            gender=voice.ssml_gender.name,
        )

@dataclass
class SynthesisRequest:
    text: str
    voice_name: str
    language_code: str
    speaking_rate: float = 1.0
