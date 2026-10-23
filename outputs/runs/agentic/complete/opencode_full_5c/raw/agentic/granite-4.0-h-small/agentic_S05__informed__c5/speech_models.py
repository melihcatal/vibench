from typing import NamedTuple
from google.cloud.speech_v1 import types
import azure.cognitiveservices.speech as speechsdk
from ibm_watson import SpeechToTextV1
import deepgram

# Define local request, response, and normalization helpers for Streaming Speech-to-Text.
# Normalizes provider-specific message formats to a common schema.


class TranscriptEvent(NamedTuple):
    """Unified representation of a transcript event (partial or final)."""

    transcript: str  # partial text
    is_final: bool
    confidence: float = None
    provider: str = None  # identifier for debugging


def normalize_google_response(
    response: types.StreamingRecognizeResponse,
) -> TranscriptEvent:
    """Convert Google Cloud StreamingRecognizeResponse to TranscriptEvent."""
    result = response.results[0]
    alt = result.alternatives[0]
    return TranscriptEvent(
        transcript=alt.transcript,
        is_final=result.is_final,
        confidence=alt.confidence,
        provider="Google Cloud",
    )


def normalize_watson_response(
    event: SpeechToTextV1.RecognizeLongRunningResponse,
) -> TranscriptEvent:
    """Convert IBM Watson streaming result to TranscriptEvent."""
    alt = event.results[0].alternatives[0]
    return TranscriptEvent(
        transcript=alt.transcript,
        is_final=event.results[0].is_final,
        confidence=alt.confidence,
        provider="IBM Watson",
    )


def normalize_azure_response(result: speechsdk.RecognitionResult) -> TranscriptEvent:
    """Convert Azure Speech streaming result to TranscriptEvent."""
    return TranscriptEvent(
        transcript=result.text,
        is_final=result.reason == speechsdk.ResultReason.RecognizedSpeech,
        confidence=result.confidence,
        provider="Azure Speech",
    )


def normalize_deepgram_response(response: dict) -> TranscriptEvent:
    """Convert Deepgram streaming JSON response to TranscriptEvent."""
    channel = response["results"][0]["alternatives"][0]
    return TranscriptEvent(
        transcript=channel["transcript"],
        is_final=channel.get("final", False),
        confidence=channel.get("confidence"),
        provider="Deepgram",
    )


def normalize_transcribe_response(event: dict) -> TranscriptEvent:
    """Placeholder for Amazon Transcribe normalization."""
    return TranscriptEvent(
        transcript=event.get("transcript", ""),
        is_final=event.get("is_final", False),
        provider="Amazon Transcribe",
    )
