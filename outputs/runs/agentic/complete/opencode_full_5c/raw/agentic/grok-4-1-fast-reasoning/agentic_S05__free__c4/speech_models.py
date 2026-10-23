from dataclasses import dataclass
from typing import Optional


@dataclass
class LiveSTTConfig:
    model: str = "nova-2"
    language: Optional[str] = "en"
    punctuate: bool = True
    interim_results: bool = True
    channels: int = 1
    sample_rate: int = 16000
    encoding: str = "linear16"
