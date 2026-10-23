"""
tts_qa_transcript.py - Transcribe synthesized QA samples to verify spoken output.

Uses Azure Cognitive Services Speech-to-Text API to transcribe TTS-generated
audio samples back to text, enabling QA comparison between original input
and actual spoken output.
Provider: Microsoft Azure Cognitive Services Speech-to-Text API
Endpoint: https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1
"""

import os
import io
import requests
from typing import Optional, Dict, Any

from speech_models import TTSResponse


# Azure Speech-to-Text configuration
AZURE_STT_REGION = os.environ.get("AZURE_STT_REGION", "eastus")
AZURE_STT_KEY = os.environ.get("AZURE_STT_KEY", "")
AZURE_STT_ENDPOINT = os.environ.get(
    "AZURE_STT_ENDPOINT",
    f"https://{AZURE_STT_REGION}.stt.speech.microsoft.com/",
)

# Azure Speech-to-Text recognition modes and locales
STT_RECOGNITION_MODES = {
    "conversation": "conversation/cognitiveservices/v1",
    "interactive": "interactive/cognitiveservices/v1",
    "dictation": "dictation/cognitiveservices/v1",
}

STT_AUDIO_FORMATS = {
    "wav_16khz": "audio/wav; codecs=audio/pcm; samplerate=16000",
    "wav_8khz": "audio/wav; codecs=audio/pcm; samplerate=8000",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg; codecs=opus",
    "flac": "audio/flac",
}


class TranscriptResult:
    """Result from Azure Speech-to-Text transcription."""

    def __init__(
        self,
        transcript: str,
        confidence: float,
        display_text: str = "",
        recognition_status: str = "",
        n_best_results: Optional[list] = None,
        raw_response: Optional[Dict[str, Any]] = None,
    ):
        self.transcript = transcript
        self.confidence = confidence
        self.display_text = display_text
        self.recognition_status = recognition_status
        self.n_best_results = n_best_results or []
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "transcript": self.transcript,
            "confidence": self.confidence,
            "display_text": self.display_text,
            "recognition_status": self.recognition_status,
            "n_best_count": len(self.n_best_results),
        }


class QAComparisonResult:
    """Result comparing original TTS text with transcribed output."""

    def __init__(
        self,
        original_text: str,
        transcribed_text: str,
        match_score: float,
        is_match: bool,
        transcript_result: Optional[TranscriptResult] = None,
    ):
        self.original_text = original_text
        self.transcribed_text = transcribed_text
        self.match_score = match_score
        self.is_match = is_match
        self.transcript_result = transcript_result

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "original_text": self.original_text,
            "transcribed_text": self.transcribed_text,
            "match_score": self.match_score,
            "is_match": self.is_match,
            "transcript_details": self.transcript_result.to_dict() if self.transcript_result else None,
        }


def transcribe_audio_bytes(
    audio_bytes: bytes,
    locale: str = "en-US",
    mode: str = "conversation",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
    audio_format: str = "wav_16khz",
) -> TranscriptResult:
    """
    Transcribe audio bytes using Azure Cognitive Services Speech-to-Text API.

    Sends audio data to the Azure Speech-to-Text REST API for recognition,
    converting synthesized speech back to text for QA verification.

    Args:
        audio_bytes: Raw audio data bytes.
        locale: Recognition locale (e.g., 'en-US').
        mode: Recognition mode ('conversation', 'interactive', 'dictation').
        region: Azure STT region override.
        subscription_key: Azure STT subscription key override.
        audio_format: Audio format identifier.

    Returns:
        TranscriptResult with transcribed text and confidence.
    """
    region = region or AZURE_STT_REGION
    key = subscription_key or AZURE_STT_KEY

    if not key:
        return TranscriptResult(
            transcript="",
            confidence=0.0,
            recognition_status="ERROR",
            raw_response={"error": "Azure STT key not configured"},
        )

    recognition_path = STT_RECOGNITION_MODES.get(mode, STT_RECOGNITION_MODES["conversation"])
    stt_endpoint = f"https://{region}.stt.speech.microsoft.com/speech/recognition/{recognition_path}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": STT_AUDIO_FORMATS.get(audio_format, STT_AUDIO_FORMATS["wav_16khz"]),
    }

    params = {
        "language": locale,
        "format": "detailed",
    }

    try:
        response = requests.post(
            stt_endpoint,
            headers=headers,
            params=params,
            data=audio_bytes,
            timeout=60,
        )
        response.raise_for_status()

        result_data = response.json()
        return _parse_stt_response(result_data)

    except requests.exceptions.RequestException as exc:
        return TranscriptResult(
            transcript="",
            confidence=0.0,
            recognition_status="ERROR",
            raw_response={"error": str(exc)},
        )


def transcribe_tts_response(
    tts_response: TTSResponse,
    original_text: str,
    locale: str = "en-US",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
) -> QAComparisonResult:
    """
    Transcribe a TTS response and compare it with the original text.

    Synthesizes audio through Azure TTS, then transcribes it back through
    Azure STT to verify the spoken output matches the intended input.

    Args:
        tts_response: TTSResponse containing Azure synthesis audio bytes.
        original_text: The original text that was synthesized.
        locale: Recognition locale.
        region: Azure STT region.
        subscription_key: Azure STT subscription key.

    Returns:
        QAComparisonResult with original vs transcribed text comparison.
    """
    if not tts_response.is_success():
        return QAComparisonResult(
            original_text=original_text,
            transcribed_text="",
            match_score=0.0,
            is_match=False,
        )

    # Transcribe the Azure TTS audio output
    transcript = transcribe_audio_bytes(
        audio_bytes=tts_response.audio_bytes,
        locale=locale,
        region=region,
        subscription_key=subscription_key,
        audio_format=_detect_audio_format(tts_response.audio_format),
    )

    # Compute match score between original and transcribed text
    match_score = _compute_text_similarity(original_text, transcript.transcript)
    is_match = match_score >= 0.85

    return QAComparisonResult(
        original_text=original_text,
        transcribed_text=transcript.transcript,
        match_score=match_score,
        is_match=is_match,
        transcript_result=transcript,
    )


def batch_transcribe_audio(
    audio_samples: list,
    locale: str = "en-US",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
) -> list:
    """
    Transcribe multiple audio samples for batch QA testing.

    Args:
        audio_samples: List of (audio_bytes, original_text) tuples.
        locale: Recognition locale.
        region: Azure STT region.
        subscription_key: Azure STT subscription key.

    Returns:
        List of QAComparisonResult objects.
    """
    results = []
    for audio_bytes, original_text in audio_samples:
        transcript = transcribe_audio_bytes(
            audio_bytes=audio_bytes,
            locale=locale,
            region=region,
            subscription_key=subscription_key,
        )
        match_score = _compute_text_similarity(original_text, transcript.transcript)
        results.append(QAComparisonResult(
            original_text=original_text,
            transcribed_text=transcript.transcript,
            match_score=match_score,
            is_match=match_score >= 0.85,
            transcript_result=transcript,
        ))
    return results


def _parse_stt_response(response_data: Dict[str, Any]) -> TranscriptResult:
    """
    Parse Azure Speech-to-Text API response into a TranscriptResult.

    The Azure STT API returns results in a specific JSON structure with
    RecognitionStatus, DisplayText, NBest, and Confidence fields.

    Args:
        response_data: Raw JSON response from Azure STT API.

    Returns:
        Parsed TranscriptResult object.
    """
    recognition_status = response_data.get("RecognitionStatus", "Unknown")
    display_text = response_data.get("DisplayText", "")
    confidence = 0.0

    n_best = response_data.get("NBest", [])
    if n_best:
        confidence = n_best[0].get("Confidence", 0.0)
    elif "Confidence" in response_data:
        confidence = response_data["Confidence"]

    return TranscriptResult(
        transcript=display_text,
        confidence=confidence,
        display_text=display_text,
        recognition_status=recognition_status,
        n_best_results=n_best,
        raw_response=response_data,
    )


def _compute_text_similarity(text_a: str, text_b: str) -> float:
    """
    Compute normalized text similarity score.

    Uses a simple token-based overlap ratio for QA comparison
    between original text and transcribed output.

    Args:
        text_a: First text string.
        text_b: Second text string.

    Returns:
        Similarity score between 0.0 and 1.0.
    """
    if not text_a or not text_b:
        return 0.0

    tokens_a = set(_normalize_text(text_a).split())
    tokens_b = set(_normalize_text(text_b).split())

    if not tokens_a and not tokens_b:
        return 1.0

    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b

    return len(intersection) / len(union) if union else 0.0


def _normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, strip punctuation)."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def _detect_audio_format(azure_format: str) -> str:
    """Map Azure TTS output format to Azure STT input format."""
    azure_format_lower = azure_format.lower()
    if "wav" in azure_format_lower or "pcm" in azure_format_lower:
        return "wav_16khz"
    if "mp3" in azure_format_lower or "mpeg" in azure_format_lower:
        return "mp3"
    if "ogg" in azure_format_lower or "opus" in azure_format_lower:
        return "ogg"
    if "flac" in azure_format_lower:
        return "flac"
    return "wav_16khz"
