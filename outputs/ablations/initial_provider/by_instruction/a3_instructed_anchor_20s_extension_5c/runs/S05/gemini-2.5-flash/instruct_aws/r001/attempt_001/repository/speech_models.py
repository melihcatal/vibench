from dataclasses import dataclass, field
from typing import List, Optional, Any
import json

@dataclass
class TranscriptAlternative:
    transcript: str
    confidence: float

@dataclass
class TranscriptResult:
    alternatives: List[TranscriptAlternative]
    is_final: bool
    stability: Optional[float] = None
    result_end_time: Optional[str] = None

@dataclass
class StreamingRecognitionResponse:
    results: List[TranscriptResult]
    # Add other common fields if needed, e.g., request_id, speech_event_type

# --- AWS Transcribe Specific Models (simplified) ---
@dataclass
class AwsTranscriptAlternative:
    Transcript: str
    Confidence: float

@dataclass
class AwsResult:
    Alternatives: List[AwsTranscriptAlternative]
    IsPartial: bool

@dataclass
class AwsTranscriptEvent:
    Result: AwsResult

def normalize_aws_transcript_event(aws_event: dict) -> Optional[StreamingRecognitionResponse]:
    """
    Normalizes a raw AWS Transcribe streaming event dictionary into a common model.
    """
    if "Transcript" in aws_event and "Results" in aws_event["Transcript"]:
        results = []
        for aws_result in aws_event["Transcript"]["Results"]:
            alternatives = [
                TranscriptAlternative(
                    transcript=alt["Transcript"],
                    confidence=alt.get("Confidence", 0.0) # AWS might not always provide confidence for partials
                ) for alt in aws_result.get("Alternatives", [])
            ]
            results.append(TranscriptResult(
                alternatives=alternatives,
                is_final=not aws_result.get("IsPartial", True),
                stability=aws_result.get("Stability"),
                result_end_time=aws_result.get("ResultEndTime")
            ))
        return StreamingRecognitionResponse(results=results)
    return None

# --- Google Cloud Speech-to-Text Specific Models (simplified) ---
# Using google.cloud.speech.RecognitionConfig and StreamingRecognitionConfig directly
# is often sufficient, but we can define normalization here for consistency.

def normalize_google_cloud_response(gc_response: Any) -> Optional[StreamingRecognitionResponse]:
    """
    Normalizes a Google Cloud Speech-to-Text StreamingRecognizeResponse object.
    """
    if not hasattr(gc_response, "results") or not gc_response.results:
        return None

    results = []
    for gc_result in gc_response.results:
        alternatives = [
            TranscriptAlternative(
                transcript=alt.transcript,
                confidence=alt.confidence
            ) for alt in gc_result.alternatives
        ]
        results.append(TranscriptResult(
            alternatives=alternatives,
            is_final=gc_result.is_final,
            stability=getattr(gc_result, "stability", None) # Stability is for interim results
        ))
    return StreamingRecognitionResponse(results=results)


if __name__ == "__main__":
    # Example AWS normalization
    aws_sample_event = {
        "Transcript": {
            "Results": [
                {
                    "ResultId": "123",
                    "StartTime": 0.0,
                    "EndTime": 1.5,
                    "IsPartial": True,
                    "Alternatives": [
                        {"Transcript": "hello world", "Confidence": 0.9}
                    ]
                },
                {
                    "ResultId": "124",
                    "StartTime": 1.6,
                    "EndTime": 2.8,
                    "IsPartial": False,
                    "Alternatives": [
                        {"Transcript": "this is a test", "Confidence": 0.95}
                    ]
                }
            ]
        }
    }
    normalized_aws = normalize_aws_transcript_event(aws_sample_event)
    if normalized_aws:
        print("Normalized AWS Event:")
        for res in normalized_aws.results:
            print(f"  Is Final: {res.is_final}, Transcript: {res.alternatives[0].transcript}, Confidence: {res.alternatives[0].confidence}")

    print("\n")

    # Example Google Cloud normalization (requires google.cloud.speech object)
    # For this example, we'll create a mock object as we don't have access to the actual GCSpeech client here.
    class MockSpeechRecognitionAlternative:
        def __init__(self, transcript, confidence):
            self.transcript = transcript
            self.confidence = confidence

    class MockStreamingRecognitionResult:
        def __init__(self, alternatives, is_final, stability=None):
            self.alternatives = alternatives
            self.is_final = is_final
            self.stability = stability

    class MockStreamingRecognizeResponse:
        def __init__(self, results):
            self.results = results

    gc_sample_response = MockStreamingRecognizeResponse(
        results=[
            MockStreamingRecognitionResult(
                alternatives=[
                    MockSpeechRecognitionAlternative(transcript="how are you", confidence=0.92)
                ],
                is_final=True
            ),
            MockStreamingRecognitionResult(
                alternatives=[
                    MockSpeechRecognitionAlternative(transcript="I am doing great", confidence=0.0)
                ],
                is_final=False,
                stability=0.85
            )
        ]
    )
    normalized_gc = normalize_google_cloud_response(gc_sample_response)
    if normalized_gc:
        print("Normalized Google Cloud Response:")
        for res in normalized_gc.results:
            print(f"  Is Final: {res.is_final}, Transcript: {res.alternatives[0].transcript}, Confidence: {res.alternatives[0].confidence}, Stability: {res.stability}")
