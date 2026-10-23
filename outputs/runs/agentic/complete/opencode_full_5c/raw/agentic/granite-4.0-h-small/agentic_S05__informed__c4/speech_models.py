import json
from typing import Dict, Any, List

# Utility helpers for request/response normalization and transformation
# Shared across same‑scenario and later‑step files.


class SpeechModels:
    """Common request/response models for streaming speech‑to‑text."""

    class RequestConfig:
        """Encapsulates configuration parameters for a streaming request."""
        def __init__(self, language: str = "en-US", punctuation: bool = True):
            self.language = language
            self.enable_punctuation = punctuation
            self.encoding = "LINEAR16"
            self.sample_rate = 16000
            self.content_type = "audio/l16;rate=16000"

        def to_dict(self) -> Dict[str, Any]:
            cfg = {"languageCode": self.language, "enableAutomaticPunctuation": self.enable_punctuation}
            # Provider‑specific overrides
            if self.encoding:
                cfg["encoding"] = self.encoding
            if self.sample_rate:
                cfg["sampleRateHertz"] = self.sample_rate
            return cfg

    class RawResult:
        """Placeholder for raw streaming results from providers."""
        def __init__(self, raw_data: Any):
            self.raw = raw_data

    @staticmethod
    def normalize(provider: str, raw: Any) -> str:
        """Convert a provider‑specific raw payload into a plain transcript string."""
        if provider == "dashscope":
            return raw.get("interim", "")
        elif provider == "google":
            alternatives = raw.get("results", [{}])[0].get("alternatives", [])
            return alternatives[0].get("transcript", "")
        elif provider == "aws":
            items = raw.get("TranscriptionResult", {}).get("Items", [])
            parts = [alt.get("Transcript", "") for itm in items for alt in itm.get("Alternatives", [{}])]
            return " ".join(parts)
        elif provider == "ibm":
            return raw.get("result", {}).get("alternatives", [{}])[0].get("transcript", "")
        elif provider == "deepgram":
            return raw["results"][0]["alternatives"][0]["transcript"]
        else:
            raise NotImplementedError(f"Normalization for {provider} not implemented")

    @staticmethod
def is_final(provider: str, raw: Any) -> bool:
        """Determine whether a streamed result marks the end of speech."""
        if provider == "dashscope":
            return raw.get("final", False)
        elif provider == "google":
            return raw.get("results", [{}])[0].get("isFinal", False)
        elif provider == "aws":
            return raw.get("IsPartial", False) == False
        elif provider == "ibm":
            return raw.get("IsPartial", False) == False
        elif provider == "deepgram":
            return raw.get("is_final", False)
        raise NotImplementedError(f"Final detection for {provider} not implemented")

if __name__ == "__main__":
    # Simple test harness – replace with real payloads
    sample_google = {
        "results": [{"alternatives": [{"transcript": "Testing", "isFinal": True}]}]
    }
    print(SpeechModels.normalize("google", sample_google))
    print(SpeechModels.is_final("google", sample_google))
