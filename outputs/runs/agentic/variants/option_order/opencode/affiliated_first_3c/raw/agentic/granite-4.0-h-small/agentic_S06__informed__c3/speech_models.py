# [HELPER] speech_models.py
# Local request, response, and normalization helpers for Text-to-Speech.

from typing import Dict, Any

# ---------- Request & Response Models ----------
# Simple dataclasses to shape inputs/outputs consistently across providers.


class TtsRequest:
    def __init__(
        self,
        text: str = "",
        ssml: str = "",
        voice_name: str = "",
        locale: str = "en-us",
    ) -> None:
        self.text = text
        self.ssml = ssml
        self.voice_name = voice_name
        self.locale = locale
        self.audio_format = "pcm_f32le"
        self.model_id = "eleven_monolingual_v1"
        # Additional provider-specific fields can be added as needed.

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "ssml": self.ssml,
            "voice_name": self.voice_name,
            "locale": self.locale,
            "audio_format": self.audio_format,
            "model_id": self.model_id,
        }


class TtsResponse:
    def __init__(self, audio_bytes: bytes, raw_response: Dict[str, Any]) -> None:
        self.audio_bytes = audio_bytes
        self.raw_response = raw_response

    def save(self, path: str) -> str:
        """Write audio to a file and return the absolute path."""
        with open(path, "wb") as f:
            f.write(self.audio_bytes)
        return path


# ---------- Normalization Helpers ----------


def normalize_locale(locale: str) -> str:
    """Convert locale string to common two‑letter format (e.g., en_US → en-us)."""
    parts = locale.split("_")
    return (
        f"{parts[0].lower()}-{parts[1].lower()}" if len(parts) == 2 else locale.lower()
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     req = TtsRequest(text="Hello, world!", voice_name="lyra")
#     cfg = req.to_dict()
#     print("Config:", cfg)
