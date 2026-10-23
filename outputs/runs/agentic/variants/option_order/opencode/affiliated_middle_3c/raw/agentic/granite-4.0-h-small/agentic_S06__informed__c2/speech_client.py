import os
from typing import Any, Dict

from azure.cognitiveservices.speech import SpeechConfig

# Azure TTS configuration (keys/region loaded from env)
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')


class SynthesisClient:
    """Thin wrapper around Azure Speech TTS providing configuration and helper utilities.

    Attributes:
        client: Low‑level Azure SDK SpeechSynthesizer instance (lazy‑initialized).
    """

    __client: Any = None

    @property
    def client(self) -> Any:
        if not self.__client:
            speech_config = SpeechConfig(
                endpoint="https://eastus.tts.speech.microsoft.com",
                subscription=AZURE_SPEECH_KEY,
                region=AZURE_SPEECH_REGION
            )
            self.__client = speech_config  # store config for reuse in other methods
        return self.__client

    def set_locale(self, locale: str) -> None:
        """Update region settings – useful for regional TTS endpoints."""
        self.client.region = locale

    def get_voices(self) -> Dict[str, Any]:
        """Retrieve list of available voices, returning Azure‑specific dict."""
        return self.client.get_voices_async().get()

    def synthesize_text(self, text: str, voice_name: str = None) -> bytes:
        """Synthesize plain text → raw PCM bytes.
        Returns: audio_bytes (16‑bit mono)"""
        audio_config = AudioConfig(output_format=AudioConfig.audio_output_format="Riff16Khz16BitMonoPcm")
        synthesizer = SpeechSynthesizer(speech_config=self.client, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()
        return result.audio_data

    def synthesize_ssml(self, ssml: str, voice_name: str = None) -> bytes:
        """Synthesize SSML → raw PCM bytes.
        Returns: audio_bytes"""
        audio_config = AudioConfig(output_format=AudioConfig.audio_output_format="Riff16Khz16BitMonoPcm")
        synthesizer = SpeechSynthesizer(speech_config=self.client, audio_config=audio_config)
        result = synthesizer.speak_ssml_async(ssml).get()
        return result.audio_data
