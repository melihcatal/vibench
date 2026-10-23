import json
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TranscriptionAlternative:
    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[dict]] = field(default_factory=list)

@dataclass
class TranscriptionResult:
    alternatives: List[TranscriptionAlternative]
    is_final: bool
    stability: Optional[float] = None

@dataclass
class StreamingRecognitionResponse:
    results: List[TranscriptionResult]
    channel_index: Optional[int] = None

def normalize_google_speech_response(response) -> StreamingRecognitionResponse:
    """Normalizes Google Cloud Speech-to-Text streaming response."""
    normalized_results = []
    for result in response.results:
        alternatives = [
            TranscriptionAlternative(
                transcript=alt.transcript,
                confidence=alt.confidence,
                # Google Cloud Speech provides word info including startTime, endTime, word
                words=[{"word": w.word, "start_time": w.start_time.seconds + w.start_time.nanos * 1e-9, "end_time": w.end_time.seconds + w.end_time.nanos * 1e-9} for w in alt.words] if hasattr(alt, 'words') else []
            )
            for alt in result.alternatives
        ]
        normalized_results.append(
            TranscriptionResult(
                alternatives=alternatives,
                is_final=result.is_final,
                stability=result.stability if hasattr(result, 'stability') else None
            )
        )
    return StreamingRecognitionResponse(results=normalized_results)

def normalize_deepgram_response(response_json: dict) -> StreamingRecognitionResponse:
    """Normalizes Deepgram streaming response."""
    normalized_results = []
    if "channel" in response_json and "alternatives" in response_json["channel"]:
        alternatives = [
            TranscriptionAlternative(
                transcript=alt.get("transcript", ""),
                confidence=alt.get("confidence"),
                words=[{"word": w.get("word"), "start_time": w.get("start"), "end_time": w.get("end")} for w in alt.get("words", [])]
            )
            for alt in response_json["channel"]["alternatives"]
        ]
        is_final = response_json.get("is_final", False)
        normalized_results.append(
            TranscriptionResult(
                alternatives=alternatives,
                is_final=is_final,
                stability=None # Deepgram might not provide a direct stability score per result
            )
        )
    return StreamingRecognitionResponse(results=normalized_results)

def normalize_aws_transcribe_event(transcript_event) -> StreamingRecognitionResponse:
    """Normalizes AWS Transcribe streaming event."""
    normalized_results = []
    if transcript_event.transcript and transcript_event.transcript.results:
        for result in transcript_event.transcript.results:
            alternatives = [
                TranscriptionAlternative(
                    transcript=alt.transcript,
                    confidence=alt.confidence,
                    # AWS Transcribe provides items which can be words
                    words=[{"word": item.content, "start_time": item.start_time, "end_time": item.end_time} for item in alt.items if item.type == 'pronunciation'] if hasattr(alt, 'items') else []
                )
                for alt in result.alternatives
            ]
            normalized_results.append(
                TranscriptionResult(
                    alternatives=alternatives,
                    is_final=not result.is_partial,
                    stability=None # AWS Transcribe might not provide a direct stability score
                )
            )
    return StreamingRecognitionResponse(results=normalized_results)
