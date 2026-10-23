from dataclasses import dataclass, asdict
from typing import Union

@dataclass
class SynthesisInputText:
    text: str

    def to_dict(self) -> dict:
        return {"text": self.text}

@dataclass
class SynthesisInputSSML:
    ssml: str

    def to_dict(self) -> dict:
        return {"ssml": self.ssml}

@dataclass
class AudioConfig:
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)