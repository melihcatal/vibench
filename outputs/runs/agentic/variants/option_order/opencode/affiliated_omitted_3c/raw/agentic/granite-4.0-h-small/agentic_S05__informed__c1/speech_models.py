# HELPER: speech_models.py
# Define local request, response, and normalization helpers for Streaming Speech-to-Text

import typing as t
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Generic streaming request payload
# ---------------------------------------------------------------------------


@dataclass
class StreamConfig:
    """Configuration for a streaming recognizer.

    Attributes:
        model (str): Model name/id (Deepgram: "nova", Google: "default", etc.)
        language (str): ISO 639‑1 language code
        punctuation (bool): Enable punctuation in results
        interim_results (bool): Request partial results
    """

    model: str
    language: str
    punctuation: bool
    interim_results: bool

    def to_dict(self) -> t.Dict[str, t.Any]:
        return {
            "model": self.model,
            "language": self.language,
            "punctuation": self.punctuation,
            "interim_results": self.interim_results,
        }

    @classmethod
    def from_dict(cls, data: t.Dict[str, t.Any]) -> "StreamConfig":
        return cls(**data)


# ---------------------------------------------------------------------------
# Normalized response structure (used by later-step files)
# ---------------------------------------------------------------------------


@dataclass
class TranscriptionResult:
    """Normalized transcription payload returned to later-step helpers.

    Attributes:
        text (str): Recognized text (partial or final)
        is_final (bool): True if this is the final result for the chunk
    """

    text: str
    is_final: bool

    @classmethod
    def from_deepgram(cls, msg: t.Dict[str, t.Any]) -> "TranscriptionResult":
        return cls(
            text=msg.get("alternatives", [{}])[0].get("transcript", ""),
            is_final=msg.get("is_final", False),
        )

    @classmethod
    def from_google(cls, resp: t.Dict[str, t.Any]) -> "TranscriptionResult":
        # Google returns SpeechRecognitionAlternative inside results[0].alternatives
        alternative = resp.get("results", [{}])[0].get("alternatives", [{}])[0]
        return cls(
            text=alternative.get("transcript", ""),
            is_final=alternative.get("is_final", False),
        )

    @classmethod
    def from_azure(cls, resp: t.Dict[str, t.Any]) -> "TranscriptionResult":
        # Azure returns display_text directly in recognition_result
        recognition = resp.get("RecognitionResult", {})
        return cls(
            text=recognition.get("display_text", ""),
            is_final=recognition.get("is_final", False),
        )


# ---------------------------------------------------------------------------
# Helper to normalize incoming messages from each provider
# ---------------------------------------------------------------------------


def normalize_message(
    provider: str, raw_msg: t.Dict[str, t.Any]
) -> t.Optional[TranscriptionResult]:
    if provider == "deepgram":
        return TranscriptionResult.from_deepgram(raw_msg)
    elif provider == "google":
        return TranscriptionResult.from_google(raw_msg)
    elif provider == "aws":
        # Amazon Transcribe streaming returns TranscriptionJob with 'Transcript'
        transcript = raw_msg.get("Transcript", {}).get("Transcript", "")
        return TranscriptionResult(text=transcript, is_final=True)
    elif provider == "azure":
        return TranscriptionResult.from_azure(raw_msg)
    return None


# ---------------------------------------------------------------------------
# Example utility functions for later steps
# ---------------------------------------------------------------------------


def request_idempotency_token() -> str:
    """Generate a unique token for idempotent streaming requests.

    In production you could use uuid.uuid4().hex"
    """
    import uuid

    return uuid.uuid4().hex


def sanitize_text(text: str) -> str:
    """Simple sanitization: strip whitespace, collapse newlines."""
    return " ".join(text.strip().split())


# ---------------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------------
