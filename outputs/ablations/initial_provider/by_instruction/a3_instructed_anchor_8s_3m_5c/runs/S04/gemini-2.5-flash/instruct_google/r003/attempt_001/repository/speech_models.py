import dataclasses

@dataclasses.dataclass
class TranscriptionConfig:
    language_code: str
    sample_rate_hertz: int
    encoding: str
