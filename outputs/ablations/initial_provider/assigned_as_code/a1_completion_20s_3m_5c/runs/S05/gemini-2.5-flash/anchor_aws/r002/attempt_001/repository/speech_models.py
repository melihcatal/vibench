from dataclasses import dataclass
from typing import AsyncGenerator, Dict, Any, Literal

@dataclass
class AudioStreamConfig:
    language_code: str
    sample_rate_hz: int
    media_encoding: Literal["pcm", "ogg", "flac"] = "pcm"
    
@dataclass
class RecognitionResult:
    text: str
    is_final: bool

def normalize_transcribe_output(event: Dict[str, Any]) -> AsyncGenerator[RecognitionResult, None]:
    for result in event["Transcript"]["Results"]:
        if result["Alternatives"]:
            yield RecognitionResult(text=result["Alternatives"][0]["Transcript"], is_final=not result["IsPartial"])
