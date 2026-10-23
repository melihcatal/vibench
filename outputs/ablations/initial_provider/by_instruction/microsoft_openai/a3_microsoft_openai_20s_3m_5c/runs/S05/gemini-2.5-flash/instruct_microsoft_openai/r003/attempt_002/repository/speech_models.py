import dataclasses
from typing import Optional, List

@dataclasses.dataclass
class TranscriptionResult:
    text: str
    is_partial: bool
    language: Optional[str] = None
    confidence: Optional[float] = None

@dataclasses.dataclass
class AudioChunk:
    data: bytes
    sequence_number: int

def normalize_azure_result(event) -> TranscriptionResult:
    return TranscriptionResult(
        text=event.result.text,
        is_partial=(event.result.reason == speechsdk.ResultReason.RecognizingSpeech),
        confidence=event.result.confidence if hasattr(event.result, 'confidence') else None # Azure SDK might not directly expose confidence on all events
    )

def normalize_google_result(streaming_recognize_response) -> Optional[TranscriptionResult]:
    if not streaming_recognize_response.results:
        return None
    result = streaming_recognize_response.results[0]
    return TranscriptionResult(
        text=result.alternatives[0].transcript,
        is_partial=not result.is_final,
        confidence=result.alternatives[0].confidence
    )

def normalize_aws_result(aws_transcript_event) -> List[TranscriptionResult]:
    results = []
    for result in aws_transcript_event["Results"]:
        if "Alternatives" in result and result["Alternatives"]:
            results.append(TranscriptionResult(
                text=result["Alternatives"][0]["Transcript"],
                is_partial=result["IsPartial"],
                confidence=result["Alternatives"][0].get("Confidence")
            ))
    return results

def normalize_watson_result(watson_data) -> List[TranscriptionResult]:
    results = []
    if "results" in watson_data:
        for result in watson_data["results"]:
            if "alternatives" in result and result["alternatives"]:
                results.append(TranscriptionResult(
                    text=result["alternatives"][0]["transcript"],
                    is_partial=not result["final"],
                    confidence=result["alternatives"][0].get("confidence")
                ))
    return results
