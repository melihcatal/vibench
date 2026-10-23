import os
import json
import logging
from typing import Dict, Any

# Helper utilities for Streaming Speech‑to‑Text
# Loads provider‑specific configuration, builds request payloads,
# and normalizes responses into a common structure.

# Config sources (in order of precedence)
ENV_CONFIG = {
    "DASHSCOPE": "DASHSCOPE_API_KEY",
    "GOOGLE": "GOOGLE_APPLICATION_CREDENTIALS",
    "AWS": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
    "IBM": ["IBM_STT_APIKEY", "IBM_STT_URL"],
    "DEEPGRAM": "DEEPGRAM_API_KEY",
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SpeechClient:
    """Base client for streaming speech recognition providers."""

    def __init__(self, provider: str):
        self.provider = provider.upper()
        self.api_key = None
        self._load_config()

    def _load_config(self):
        env_vars = ENV_CONFIG.get(self.provider)
        if not env_vars:
            raise ValueError(f"Unsupported provider: {self.provider}")
        for ev in env_vars if isinstance(env_vars, list) else [env_vars]:
            self.api_key = os.getenv(ev)
            if self.api_key:
                logger.info(f"Loaded API key for {self.provider} from ${ev}")
                return
        raise ValueError(
            f"Environment variable(s) {env_vars} not set for {self.provider}"
        )

    def _build_config_payload(
        self, language: str = "en-US", punctuation: str = "on"
    ) -> Dict[str, Any]:
        """Return provider‑specific configuration payload."""
        cfg = {
            "languageCode": language,
            "enableAutomaticPunctuation": punctuation.lower() == "on",
        }
        # Example: Google expects `model` and `use_enhanced`
        if self.provider == "GOOGLE":
            cfg["encoding"] = "LINEAR16"
            cfg["sampleRateHertz"] = 16000
        return cfg

    def _normalize_response(self, raw: Any) -> str:
        """Convert provider‑specific response into a plain transcript string."""
        if self.provider == "DASHSCOPE":
            # DashScope returns interim text under `interim`
            return raw.get("interim", "")
        elif self.provider == "GOOGLE":
            # Google returns a list of alternatives
            alternatives = raw.get("results", [{}])[0].get("alternatives", [])
            return alternatives[0].get("transcript", "")
        elif self.provider == "AWS":
            # Amazon Transcribe returns Items with Alternatives
            items = raw.get("TranscriptionResult", {}).get("Items", [])
            parts = [
                alt.get("Transcript", "")
                for itm in items
                for alt in itm.get("Alternatives", [{}])
            ]
            return " ".join(parts)
        elif self.provider == "IBM":
            # Watson returns interim results in the callback payload
            return (
                raw.get("result", {}).get("alternatives", [{}])[0].get("transcript", "")
            )
        elif self.provider == "DEEPGRAM":
            return raw["results"][0]["alternatives"][0]["transcript"]
        else:
            raise NotImplementedError(
                f"Normalization for {self.provider} not implemented"
            )


if __name__ == "__main__":
    # Demo usage
    client = SpeechClient("google")
    dummy_response = {"results": [{"alternatives": [{"transcript": "Hello world"}]}]}
    print(client._normalize_response(dummy_response))
