# [HELPER] speech_client.py
# Local configuration and helper utilities for Text-to-Speech providers
import os
from typing import Dict, Any, Optional

# Provider selection constants (add more as needed)
PROVIDER_AZURE = "azure"

# Default provider (can be overridden via env var or config)
DEFAULT_PROVIDER = os.getenv("TTS_PROVIDER", PROVIDER_AZURE)


def load_provider_config(provider: str) -> Dict[str, Any]:
    """Load provider-specific configuration from env variables."""
    if provider == PROVIDER_AZURE:
        return {
            "key": os.getenv("AZURE_SPEECH_KEY"),
            "region": os.getenv("AZURE_SPEECH_REGION"),
        }
    raise ValueError(f"Unsupported provider: {provider}")


class SpeechClient:
    """Central client wrapper that delegates to provider-specific implementations."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or DEFAULT_PROVIDER
        cfg = load_provider_config(self.provider)
        self.config = cfg
        self._init_provider()

    def _init_provider(self) -> None:
        if self.provider == PROVIDER_AZURE:
            from azure.cognitiveservices.speech import SpeechConfig

            self._speech_config = SpeechConfig(
                subscription=self.config["key"],
                region=self.config["region"],
            )
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

    def get_config(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "config": self._speech_config if self.provider == PROVIDER_AZURE else None,
        }

    def synthesize_text(
        self, text: str, voice_name: str = "en-US-JennyNeural"
    ) -> bytes:
        if self.provider == PROVIDER_AZURE:
            from azure.cognitiveservices.speech import AudioConfig, SpeechSynthesizer

            audio_config = AudioConfig(output_format="Mp3")
            synthesizer = SpeechSynthesizer(
                speech_config=self._speech_config,
                audio_config=audio_config,
            )
            result = synthesizer.speak_text_async(text).get()
            if result.reason == result.reasons_success:
                return result.audio_data
            else:
                raise RuntimeError(f"Azure TTS failed: {result.reason}")
        else:
            raise NotImplementedError(
                f"Provider {self.provider} synthesize not implemented"
            )
