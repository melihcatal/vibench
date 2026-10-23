from dataclasses import dataclass
from typing import Optional


@dataclass
class STTConfig:
    model: str = "nova-2"
    language: Optional[str] = "en"
    punctuate: bool = True
    interim_results: bool = True
