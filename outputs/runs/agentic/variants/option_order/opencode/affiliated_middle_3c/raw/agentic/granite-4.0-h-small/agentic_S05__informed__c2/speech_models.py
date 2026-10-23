from typing import TypedDict, List


class SpeechRecognitionResult(TypedDict):
    transcript: str
    is_final: bool
    alternatives: List[dict]


def normalize_transcript(raw_result: SpeechRecognitionResult) -> str:
    """Extracts the best transcript from a raw recognition result.
    Supports Deepgram, Amazon Transcribe, and Watson STT structures.
    Args:
        raw_result (SpeechRecognitionResult): raw response from provider
    Returns:
        str: normalized transcript
    """
    # Deepgram example: alternatives[0].transcript
    alt = raw_result.get("alternatives", [{}])[0]
    return alt.get("transcript", "")


# Example utility functions for other services would be added similarly.
