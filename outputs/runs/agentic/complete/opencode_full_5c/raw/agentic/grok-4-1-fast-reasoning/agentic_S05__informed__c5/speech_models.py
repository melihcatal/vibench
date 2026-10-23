from typing import TypedDict, AsyncIterator, Dict, Any


class TranscriptChunk(TypedDict):
    transcript: str
    is_final: bool
    confidence: float | None


TranscriptStream = AsyncIterator[TranscriptChunk]

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_FRAME_SIZE = 1024


class LiveOptions(Dict[str, Any]):
    model: str = "nova-2"
    language: str = "en"
    punctuate: bool = True
    interim_results: bool = True
