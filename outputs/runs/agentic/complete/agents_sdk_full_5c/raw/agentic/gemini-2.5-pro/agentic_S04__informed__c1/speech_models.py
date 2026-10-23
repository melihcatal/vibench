from typing import List, Optional
from pydantic import BaseModel

class TranscriptionJob(BaseModel):
    id: str
    status: str

class TranscriptSegment(BaseModel):
    text: str
    start: int
    end: int
    speaker: Optional[str] = None

class FullTranscript(BaseModel):
    id: str
    text: str
    segments: List[TranscriptSegment]
