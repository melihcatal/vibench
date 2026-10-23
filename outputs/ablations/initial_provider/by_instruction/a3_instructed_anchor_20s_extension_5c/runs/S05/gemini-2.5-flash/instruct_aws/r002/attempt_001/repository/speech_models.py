
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Alternative:
    transcript: str
    confidence: float = 0.0
    words: Optional[List[Dict[str, Any]]] = None # To hold word-level details if available

@dataclass
class SpeechRecognitionResult:
    alternatives: List[Alternative]
    is_final: bool
    stability: float = 0.0 # Google Cloud specific
    channel_tag: Optional[int] = None # For multi-channel audio

@dataclass
class SpeechRecognitionEvent:
    results: List[SpeechRecognitionResult]
    event_type: str = "transcript" # e.g., "transcript", "no_match", "error"

def normalize_aws_transcribe_result(aws_transcribe_event: Dict[str, Any]) -> Optional[SpeechRecognitionEvent]:
    """
    Normalizes a raw AWS Transcribe event dictionary into a SpeechRecognitionEvent.
    """
    if "TranscriptEvent" in aws_transcribe_event:
        transcript_data = aws_transcribe_event["TranscriptEvent"]["Transcript"]
        results = []
        for aws_result in transcript_data.get("Results", []):
            alternatives = []
            for aws_alternative in aws_result.get("Alternatives", []):
                alternatives.append(
                    Alternative(
                        transcript=aws_alternative.get("Transcript", ""),
                        confidence=aws_alternative.get("Confidence", 0.0),
                        # AWS Transcribe provides word-level information in `Items`
                        # This would require more complex parsing if needed
                        words=[{"content": item["Content"], "start_time": item["StartTime"], "end_time": item["EndTime"], "type": item["Type"]} for item in aws_alternative.get("Items", []) if item["Type"] == "pronunciation"]
                    )
                )
            results.append(
                SpeechRecognitionResult(
                    alternatives=alternatives,
                    is_final=not aws_result.get("IsPartial", True)
                )
            )
        return SpeechRecognitionEvent(results=results, event_type="transcript")
    return None

def normalize_google_speech_result(google_speech_response: Any) -> Optional[SpeechRecognitionEvent]:
    """
    Normalizes a raw Google Cloud Speech-to-Text response object into a SpeechRecognitionEvent.
    """
    # google_speech_response is typically an object from the SDK, not a dict
    if not google_speech_response or not google_speech_response.results:
        return None

    results = []
    for google_result in google_speech_response.results:
        alternatives = []
        for google_alternative in google_result.alternatives:
            alternatives.append(
                Alternative(
                    transcript=google_alternative.transcript,
                    confidence=google_alternative.confidence,
                    words=[
                        {"content": word.word, "start_time": word.start_time.seconds + word.start_time.nanos / 1e9, "end_time": word.end_time.seconds + word.end_time.nanos / 1e9}
                        for word in google_alternative.words
                    ] if hasattr(google_alternative, 'words') else None
                )
            )
        results.append(
            SpeechRecognitionResult(
                alternatives=alternatives,
                is_final=google_result.is_final,
                stability=google_result.stability
            )
        )
    return SpeechRecognitionEvent(results=results, event_type="transcript")

# Azure Speech SDK results are processed in callbacks, so direct normalization of a
# full response object might be less common. However, we can define a structure
# for normalized results coming from Azure.
def normalize_azure_speech_result(azure_result_text: str, is_final: bool) -> SpeechRecognitionEvent:
    """
    Normalizes a simple Azure Speech SDK result (text and finality) into a SpeechRecognitionEvent.
    """
    alternative = Alternative(transcript=azure_result_text)
    result = SpeechRecognitionResult(alternatives=[alternative], is_final=is_final)
    return SpeechRecognitionEvent(results=[result], event_type="transcript")
