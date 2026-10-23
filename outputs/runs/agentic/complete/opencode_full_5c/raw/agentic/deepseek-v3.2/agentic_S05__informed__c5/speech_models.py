from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class SpeechResult:
    """Define speech recognition result with metadata."""

    text: str
    is_final: bool
    confidence: Optional[float] = None
    language: str = "en-US"
    timestamp: Optional[datetime] = None
    word_timestamps: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "text": self.text,
            "is_final": self.is_final,
            "confidence": self.confidence,
            "language": self.language,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "word_timestamps": self.word_timestamps,
        }

    @classmethod
    def from_azure_result(cls, azure_result, is_final: bool = True):
        """Create SpeechResult from Azure Speech SDK result."""
        from datetime import datetime

        word_timestamps = None
        if hasattr(azure_result, "words") and azure_result.words:
            word_timestamps = []
            for word in azure_result.words:
                word_timestamps.append(
                    {
                        "word": word.word,
                        "offset": word.offset,
                        "duration": word.duration,
                        "confidence": getattr(word, "confidence", None),
                    }
                )

        return cls(
            text=azure_result.text,
            is_final=is_final,
            confidence=getattr(azure_result, "confidence", None),
            timestamp=datetime.now(),
            word_timestamps=word_timestamps,
        )


@dataclass
class StreamingConfig:
    """Configuration for streaming speech recognition."""

    language: str = "en-US"
    enable_punctuation: bool = True
    enable_word_timestamps: bool = True
    profanity_filter: str = "masked"  # "masked", "removed", or "raw"
    sample_rate: int = 16000
    channels: int = 1
    bits_per_sample: int = 16

    def validate(self) -> bool:
        """Validate configuration parameters."""
        from speech_client import get_speech_client

        client = get_speech_client()
        supported_languages = client.get_supported_languages()

        if self.language not in supported_languages:
            raise ValueError(f"Language {self.language} not supported")

        if self.profanity_filter not in ["masked", "removed", "raw"]:
            raise ValueError(f"Profanity filter {self.profanity_filter} not supported")

        client.validate_audio_format(
            sample_rate=self.sample_rate,
            channels=self.channels,
            bits_per_sample=self.bits_per_sample,
        )

        return True


class TranscriptNormalizer:
    """Helper for normalizing transcript text."""

    @staticmethod
    def normalize_punctuation(text: str) -> str:
        """Normalize punctuation in transcript text."""
        # Add space after punctuation if missing
        import re

        text = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", text)

        # Ensure proper spacing around commas
        text = re.sub(r"\s*,\s*", ", ", text)

        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]

        return text.strip()

    @staticmethod
    def remove_fillers(text: str) -> str:
        """Remove common filler words from transcript."""
        fillers = ["um", "uh", "like", "you know", "I mean", "actually", "basically"]

        for filler in fillers:
            # Remove filler words with surrounding spaces
            pattern = r"\s+" + re.escape(filler) + r"\s+"
            text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

            # Remove filler at beginning
            pattern = r"^" + re.escape(filler) + r"\s+"
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

            # Remove filler at end
            pattern = r"\s+" + re.escape(filler) + r"$"
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        return text.strip()

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Split transcript into sentences."""
        import re

        # Simple sentence splitting
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences


class ResponseParser:
    """Parse and process speech recognition responses."""

    @staticmethod
    def parse_azure_response(evt, is_final: bool = True) -> Optional[SpeechResult]:
        """Parse Azure Speech SDK event into SpeechResult."""
        from speech_client import get_speech_client

        client = get_speech_client()

        if evt.result.reason == client.speech.ResultReason.RecognizedSpeech:
            return SpeechResult.from_azure_result(evt.result, is_final)
        elif (
            evt.result.reason == client.speech.ResultReason.RecognizingSpeech
            and not is_final
        ):
            # Partial result
            result = SpeechResult(
                text=evt.result.text, is_final=False, timestamp=datetime.now()
            )
            return result

        return None

    @staticmethod
    def merge_partial_results(partial_results: List[SpeechResult]) -> str:
        """Merge multiple partial results into a coherent transcript."""
        if not partial_results:
            return ""

        # Sort by timestamp if available
        sorted_results = sorted(
            partial_results, key=lambda x: x.timestamp if x.timestamp else datetime.min
        )

        # Get the most recent complete thought
        merged_text = sorted_results[-1].text if sorted_results else ""

        return merged_text

    @staticmethod
    def calculate_confidence_metrics(results: List[SpeechResult]) -> Dict[str, Any]:
        """Calculate confidence metrics from recognition results."""
        if not results:
            return {"average_confidence": 0, "total_results": 0}

        final_results = [r for r in results if r.is_final and r.confidence is not None]

        if not final_results:
            return {"average_confidence": 0, "total_results": 0}

        avg_confidence = sum(r.confidence for r in final_results) / len(final_results)

        return {
            "average_confidence": avg_confidence,
            "total_results": len(results),
            "final_results": len(final_results),
            "partial_results": len([r for r in results if not r.is_final]),
        }
