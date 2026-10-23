from typing import Literal, Dict, Any
from dataclasses import dataclass, field


@dataclass
class SynthesisPayload:
    text: str | None = None
    ssml: str | None = None
    voice_name: str = 'en-US-JennyNeural'
    output_format: str = 'Audio16Khz32KBitRateMonoMp3'

    def __post_init__(self):
        if not self.text and not self.ssml:
            raise ValueError("Either 'text' or 'ssml' must be provided.")
        if self.text and self.ssml:
            raise ValueError("Cannot provide both 'text' and 'ssml'.")


@dataclass
class VoiceSelection:
    locale: str = 'en-US'
    gender: Literal['Male', 'Female', None] = None


@dataclass
class SynthesisConfig:
    api_key: str = field(default_factory=lambda: os.environ.get('AZURE_SPEECH_KEY'))
    region: str = field(default_factory=lambda: os.environ.get('AZURE_SPEECH_REGION'))
    voice: str | None = None

