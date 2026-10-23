from typing import Dict, Any, Optional


class SpeechNormalizer:
    @staticmethod
    def normalize_transcript(event: Dict[str, Any]) -> Optional[str]:
        if not event:
            return None
        return (
            event.get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
        )


class SpeechRequestBuilder:
    @staticmethod
    def build_options(
        language: str = "en-US",
        punctuate: bool = True,
        interim_results: bool = True,
        model: str = "general",
    ) -> dict:
        return {
            "language": language,
            "punctuate": punctuate,
            "interim_results": interim_results,
            "model": model,
        }


class SpeechResponse:
    def __init__(self, event: Dict[str, Any]):
        self.event = event
        self.transcript = SpeechNormalizer.normalize_transcript(event)
        self.is_final = event.get("is_final", False)
        self.type = "final" if self.is_final else "interim"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "text": self.transcript,
            "is_final": self.is_final,
        }
