from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TranscriptAlternative(BaseModel):
    transcript: str
    confidence: Optional[float] = None

class TranscriptResult(BaseModel):
    alternatives: List[TranscriptAlternative]
    is_partial: bool
    start_time: Optional[float] = None
    end_time: Optional[float] = None

class TranscriptSegment(BaseModel):
    text: str
    is_final: bool
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    alternatives: Optional[List[TranscriptAlternative]] = None

class StreamingRecognitionConfig(BaseModel):
    language_code: str
    sample_rate_hz: int
    media_encoding: str = "pcm"
    
class StreamAudioPayload(BaseModel):
    audio_chunks: List[bytes]
    language_code: str
    sample_rate_hz: int
