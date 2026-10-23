import os
from typing import Optional

# Azure Speech SDK import (concrete provider signal)
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

# Environment variables for authentication
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

if not AZURE_SPEECH_KEY:
    raise RuntimeError("Set AZURE_SPEECH_KEY environment variable before using the TTS client")

# Helper to create a reusable SpeechSynthesizer instance
class TtsClient:
    def __init__(self) -> None:
        self.speech_config = SpeechConfig(
            subscription=AZURE_SPEECH_KEY,
            region=AZURE_SPEECH_REGION,
        )
        # Default language used when none specified in higher‑level calls
        self.speech_config.speech_synthesis_language = "en-US"
        self.audio_config = AudioConfig(use_default_microphone=False)
        self.synthesizer = SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=self.audio_config
        )

    def synthesize_speech(
        self,
        speech_config: dict,
        audio_config: dict,
        text: str,
    ) -> any:
        # Merge caller‑provided config with defaults
        cfg = dict(self.speech_config.__dict__)
        cfg.update(speech_config)
        opts = AudioConfig(format_=audio_config["Format"])
        result = self.synthesizer.speak_text_async(text).get()
        return result

    def list_voices(self, locale: str = "en-US") -> any:
        return self.synthesizer.voices_list(locale)

# Singleton client instance
_tts_client = TtsClient()

def get_tts_client() -> TtsClient:
    """Return the shared TTS client instance."""
    return _tts_client

if __name__ == "__main__":
    # Quick demo: list voices for en-US and synthesize a hello world
    voices = get_tts_client().list_voices()
    print([v.display_name for v in voices[:5]])
