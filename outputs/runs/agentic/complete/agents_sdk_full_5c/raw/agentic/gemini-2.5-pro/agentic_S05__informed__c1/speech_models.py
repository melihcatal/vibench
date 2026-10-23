from typing import TypedDict, List

class Word(TypedDict):
    word: str
    start: float
    end: float
    confidence: float
    punctuated_word: str

class Alternative(TypedDict):
    transcript: str
    confidence: float
    words: List[Word]

class Channel(TypedDict):
    alternatives: List[Alternative]

class UtteranceEnd(TypedDict):
    type: str

class StreamingTranscript(TypedDict):
    type: str
    channel: Channel
    start: float
    is_final: bool
    speech_final: bool
    duration: float
    metadata: dict
