from dataclasses import dataclass
from google.cloud.speech_v1p1beta1 import types

@dataclass
class TranscriptChunk:
    text: str
    is_final: bool
    confidence: float

def parse_gcsst_response(result: types.SpeechRecognitionResult, alternative: types.SpeechRecognitionAlternative) -> TranscriptChunk:
    """Parses a Google Cloud Speech-to-Text result and alternative into a TranscriptChunk.

    Args:
        result: The SpeechRecognitionResult object.
        alternative: The SpeechRecognitionAlternative object.

    Returns:
        TranscriptChunk: An object containing the transcript text, finality, and confidence.
    """
    if alternative and alternative.transcript:
        return TranscriptChunk(
            text=alternative.transcript,
            is_final=result.is_final,
            confidence=alternative.confidence if alternative.confidence else 0.0
        )
    return None
