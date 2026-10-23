from typing import Any, Dict, List, Optional


class BatchTranscriptionResponse:
    """Normalized response model for batch transcription results across providers.

    Attributes:
        job_id (str): Original job identifier.
        status (str): Final job status (e.g., COMPLETED, FAILED).
        transcript (List[Dict]): List of word/segment objects with timing and confidence.
    """

    def __init__(self, raw_response: Dict[str, Any]) -> None:
        self.job_id = raw_response.get("TranscriptionJobName")
        self.status = raw_response.get("TranscriptionJob").get("TranscriptionJobStatus")
        self.transcript = self._normalize_transcript(raw_response)

    @staticmethod
    def _normalize_transcript(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Amazon Transcribe items -> standardized format
        items = raw.get("TranscriptionJob", {}).get("Transcript", {}).get("Items", [])
        normalized = []
        for item in items:
            normalized.append(
                {
                    "start_time": item.get("StartTimestamp"),
                    "end_time": item.get("EndTimestamp"),
                    "confidence": item.get("Confidence"),
                    "alternatives": [
                        alt.get("Transcript") for alt in item.get("Alternatives", [])
                    ],
                }
            )
        return normalized


class TranslationRequest:
    """Payload model for translation requests (provider-agnostic)."""

    def __init__(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "es",
        context: Optional[str] = None,
    ) -> None:
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.context = context


class TranslationResponse:
    """Normalized translation result container."""

    def __init__(self, translated_text: str, raw: Any = None) -> None:
        self.translated_text = translated_text
        self.raw = raw  # preserve original provider-specific payload if needed


class ModerationRequest:
    """Payload for content moderation (simple text-based)."""

    def __init__(self, text: str) -> None:
        self.text = text


class ModerationResponse:
    """Container for moderation verdicts."""

    def __init__(
        self,
        is_blocked: bool = False,
        reasons: Optional[List[str]] = None,
        raw: Any = None,
    ) -> None:
        self.is_blocked = is_blocked
        self.reasons = reasons or []
        self.raw = raw


class SummarizationRequest:
    """Input for generating a summary of transcript segments."""

    def __init__(
        self, transcript_segments: List[Dict[str, Any]], max_length: int = 200
    ) -> None:
        self.segments = transcript_segments
        self.max_length = max_length


class SummarizationResponse:
    """Container for generated summary text."""

    def __init__(self, summary: str, raw: Any = None) -> None:
        self.summary = summary
        self.raw = raw


class EmbeddingRequest:
    """Request model for segment embeddings."""

    def __init__(self, segments: List[str]) -> None:
        self.segments = segments


class EmbeddingResponse:
    """Container for embedding vectors (list of float arrays)."""

    def __init__(self, embeddings: List[List[float]], raw: Any = None) -> None:
        self.embeddings = embeddings
        self.raw = raw
