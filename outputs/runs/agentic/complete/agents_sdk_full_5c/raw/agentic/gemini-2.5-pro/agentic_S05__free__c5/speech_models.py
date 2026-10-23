from dataclasses import dataclass
from typing import List

# Audio stream configuration
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

@dataclass
class TranscriptResult:
    """A simple data class to hold transcript information."""
    transcript: str
    is_final: bool
    stability: float
    confidence: float

def normalize_google_response(response) -> List[TranscriptResult]:
    """Converts a Google Speech API response to a list of TranscriptResult objects."""
    results = []
    for res in response.results:
        if not res.alternatives:
            continue
        
        alternative = res.alternatives[0]
        results.append(
            TranscriptResult(
                transcript=alternative.transcript,
                is_final=res.is_final,
                stability=res.stability,
                confidence=alternative.confidence,
            )
        )
    return results
