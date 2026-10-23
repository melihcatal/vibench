from typing import List, Optional
from dataclasses import dataclass

@dataclass
class WordInfo:
    text: str
    start: int # milliseconds
    end: int # milliseconds
    speaker: Optional[str] = None
    confidence: Optional[float] = None

@dataclass
class TranscriptResult:
    id: str
    text: str
    status: str
    words: Optional[List[WordInfo]] = None
    audio_url: Optional[str] = None

def normalize_assemblyai_transcript(assemblyai_transcript) -> TranscriptResult:
    """Normalizes an AssemblyAI transcript object into a local TranscriptResult."""
    words_info = []
    if hasattr(assemblyai_transcript, 'words') and assemblyai_transcript.words:
        for word in assemblyai_transcript.words:
            words_info.append(WordInfo(
                text=word.text,
                start=word.start,
                end=word.end,
                speaker=getattr(word, 'speaker', None),
                confidence=getattr(word, 'confidence', None),
            ))
    return TranscriptResult(
        id=assemblyai_transcript.id,
        text=assemblyai_transcript.text,
        status=assemblyai_transcript.status.value, # AssemblyAI status is an enum
        words=words_info,
        audio_url=assemblyai_transcript.audio_url,
    )
