import os
import dashscope

class SpeechClient:
    """
    Central helper for Text‑to‑Speech operations. Handles configuration,
    client instantiation and reusable utility methods.
    """
    API_KEY = os.getenv("DASHSCOPE_API_KEY", "${DASHSCOPE_API_KEY}")

    def __init__(self):
        # Dashboard client (CosyVoice TTS example)
        self.client = dashscope.TextToSpeech(api_key=self.API_KEY)

    def synthesize_plain(self, text: str, voice: str = None, **kwargs):
        """Synthesize plain text to audio bytes (uses CosyVoice)."""
        params = {
            "text": text,
            "format": "audio-8khz-16bit-mono"
        }
        if voice:
            params["voice"] = voice
        response = self.client.cosy_voice(**params)
        return response.audio_bytes

    def synthesize_ssml(self, ssml: str, **kwargs):
        """Synthesize SSML. The underlying provider may require special markup """
        params = {
            "text": ssml,
            "format": "audio-8khz-16bit-mono"
        }
        response = self.client.cosy_voice(**params)
        return response.audio_bytes

    # Add more helper methods (e.g., list_voices, upload_audio) as needed.

# Convenience singleton for simple scripts
client = SpeechClient()
