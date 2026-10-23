from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TranscriptionProperties:
    wordLevelTimestampsEnabled: Optional[bool] = False
    diarizationEnabled: Optional[bool] = False
    languageIdentification: Optional[dict] = None
    # Add other properties as needed

@dataclass
class TranscriptionRequest:
    displayName: str
    locale: str
    contentUrls: List[str]
    properties: TranscriptionProperties = field(default_factory=TranscriptionProperties)

@dataclass
class TranscriptionResult:
    id: str
    status: str
    locale: str
    createdDateTime: str
    lastActionDateTime: str
    displayName: str
    links: dict = field(default_factory=dict)
    properties: dict = field(default_factory=dict)

@dataclass
class TranscriptionFile:
    kind: str
    properties: dict
    self: str

@dataclass
class WordLevelTimestamp:
    word: str
    offset: int # in ticks (100-nanosecond units)
    duration: int # in ticks (100-nanosecond units)

@dataclass
class DiarizationSpeaker:
    speaker: int
    offset: int
    duration: int
    text: str

# Helper to convert Azure's ticks to seconds
def ticks_to_seconds(ticks: int) -> float:
    return ticks / 10000000.0
