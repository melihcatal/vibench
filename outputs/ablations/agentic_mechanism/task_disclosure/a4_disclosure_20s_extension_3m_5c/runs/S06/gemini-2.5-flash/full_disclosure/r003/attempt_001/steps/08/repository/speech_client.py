import os
import requests
import json

class SpeechClientConfig:
    """
    Provides local configuration for Text-to-Speech services.
    """
    def __init__(self):
        self.api_key = os.environ.get("TTS_API_KEY", "YOUR_DEFAULT_API_KEY")
        self.base_url = os.environ.get("TTS_BASE_URL", "https://api.example.com/tts/v1")
        self.output_format = os.environ.get("TTS_OUTPUT_FORMAT", "mp3")

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

class SpeechClient:
    """
    Provides client helper utilities for Text-to-Speech services.
    """
    def __init__(self, config: SpeechClientConfig = None):
        self.config = config if config else SpeechClientConfig()

    def synthesize_text(self, text: str, voice_id: str = "default-voice", speed: float = 1.0):
        """
        Synthesizes plain text to an audio byte stream using the configured TTS service.
        This is a placeholder for actual API interaction.
        """
        if not text:
            raise ValueError("Text cannot be empty.")

        payload = {
            "text": text,
            "voice_id": voice_id,
            "speed": speed,
            "output_format": self.config.output_format
        }
        try:
            response = requests.post(
                f"{self.config.base_url}/synthesize",
                headers=self.config.get_headers(),
                data=json.dumps(payload)
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error during text synthesis: {e}")
            return None

    def list_voices(self, locale: str = "en-US"):
        """
        Lists available voices for a target locale.
        This is a placeholder for actual API interaction.
        """
        try:
            response = requests.get(
                f"{self.config.base_url}/voices",
                headers=self.config.get_headers(),
                params={"locale": locale}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing voices: {e}")
            return []
