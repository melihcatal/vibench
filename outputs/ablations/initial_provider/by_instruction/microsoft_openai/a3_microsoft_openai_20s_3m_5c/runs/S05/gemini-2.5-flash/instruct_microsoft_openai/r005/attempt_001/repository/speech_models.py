from typing import Literal, TypedDict, Optional, List

# This file defines local request, response, and normalization helpers
# for Streaming Speech-to-Text tasks.

class InterimTranscript(TypedDict):
    interim_transcript: str

class FinalTranscript(TypedDict):
    final_transcript: str

SpeechRecognitionResult = TypedDict(
    "SpeechRecognitionResult",
    {
        "interim_transcript": Optional[str],
        "final_transcript": Optional[str],
        "language_code": Optional[str],
        "is_partial": bool,
        "confidence": Optional[float],
    },
    total=False,
)

class TranscriptionConfig(TypedDict, total=False):
    language_code: str
    enable_automatic_punctuation: bool
    sample_rate_hertz: int
    encoding: Literal["LINEAR16", "FLAC", "MULAW"]
    # Add other common configuration parameters as needed

class TranslationResult(TypedDict):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

class SafetyCheckResult(TypedDict):
    text: str
    is_safe: bool
    moderation_details: Optional[Dict]

class MeetingSummaryResult(TypedDict):
    transcript_chunk: str
    summary: str

class CaptionEmbeddingResult(TypedDict):
    caption_chunk: str
    embedding: List[float]

def normalize_transcript_result(raw_result: Dict, provider: str) -> SpeechRecognitionResult:
    """Normalizes raw transcription results from different providers into a common format."""
    normalized: SpeechRecognitionResult = {"is_partial": False}

    if provider == "openai":
        # OpenAI Whisper API typically provides final transcripts post-processing
        # For streaming, this is a conceptual placeholder.
        if "text" in raw_result:
            normalized["final_transcript"] = raw_result["text"]
            normalized["is_partial"] = False # Assuming OpenAI provides final results
        # If we were simulating interim, we'd add logic here.

    elif provider == "google_cloud":
        if "interim_transcript" in raw_result:
            normalized["interim_transcript"] = raw_result["interim_transcript"]
            normalized["is_partial"] = True
        elif "final_transcript" in raw_result:
            normalized["final_transcript"] = raw_result["final_transcript"]
            normalized["is_partial"] = False

    elif provider == "assemblyai":
        if "interim_transcript" in raw_result:
            normalized["interim_transcript"] = raw_result["interim_transcript"]
            normalized["is_partial"] = True
        elif "final_transcript" in raw_result:
            normalized["final_transcript"] = raw_result["final_transcript"]
            normalized["is_partial"] = False
    
    elif provider == "aws_transcribe":
        if "interim_transcript" in raw_result:
            normalized["interim_transcript"] = raw_result["interim_transcript"]
            normalized["is_partial"] = True
        elif "final_transcript" in raw_result:
            normalized["final_transcript"] = raw_result["final_transcript"]
            normalized["is_partial"] = False

    return normalized
