from dataclasses import dataclass, field
from typing import Optional

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = "en-US-Standard-A"
    audio_encoding: str = "MP3"

    def __post_init__(self):
        if not self.text and not self.ssml:
            raise ValueError("Either 'text' or 'ssml' must be provided.")
        if self.text and self.ssml:
            raise ValueError("Cannot provide both 'text' and 'ssml'.")

@dataclass
class VoiceInfo:
    name: str
    language_codes: list[str]
    ssml_gender: str
    natural_sample_rate_hertz: int

