import os
import json
import time
from speech_models import SpeechRequest, SpeechResponse


class SpeechModels:
    """Utility class providing static helpers for request/response shaping and normalization."""

    # Mapping of internal voice names to provider‑specific identifiers (example for Google)
    VOICE_MAP = {
        "en-us_wavenet_d": "en-US-Wavenet-D",
        "en-gb_aisha": "en-GB-Standard-A",
        "es-es_antonio": "es-ES-Standard-A",
    }

    @staticmethod
    def normalize_voice_selection(voice_name: str, language_code: str) -> str:
        """Return a provider‑compatible voice identifier from an internal name."""
        key = f"{language_code.lower()}_{voice_name.lower()}"
        return SpeechModels.VOICE_MAP.get(key, voice_name)

    @staticmethod
    def build_gcs_output_url(base_bucket: str, filename: str) -> str:
        """Construct a GCS object path from bucket and filename."""
        return f"gs://{base_bucket}/{filename}"

    @staticmethod
    def parse_api_response(sdk_response) -> SpeechResponse:
        """Convert any SDK's SynthesizeSpeechResponse into a unified SpeechResponse."""
        return SpeechResponse(
            audio_content=sdk_response.audio_content,
            content_type="audio/wav",
            duration_seconds=time.time(),  # placeholder for actual audio duration extraction
        )

    @staticmethod
    def request_from_json(json_blob: dict) -> SpeechRequest:
        """Create a SpeechRequest from a generic JSON payload used across later‑step scripts."""
        return SpeechRequest(
            text=json_blob.get("text", ""),
            ssml=json_blob.get("ssml", ""),
            voice=json_blob.get("voice", None),
            language_code=json_blob.get("language_code", "en-US"),
            output_path=json_blob.get("output_path", None),
        )
