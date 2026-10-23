from dataclasses import dataclass


@dataclass
class STTConfig:
    language: str = "en"
    punctuate: bool = True
    interim_results: bool = True
    model: str = "nova-2"
