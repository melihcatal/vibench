import os
from google.cloud import texttospeech


class TextToSpeechClient:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/gcp/credentials.json"
        )
        self.client = texttospeech.TextToSpeechClient()
        # Pre‑load a default voice for fallback
        self.default_voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Wavenet-D"
        )

    def synthesize_speech(
        self, input_text: str, voice_name: str = None, language_code: str = "en-US"
    ) -> texttospeech.SynthesizeSpeechResponse:
        """Synthesize plain text to audio using Google Cloud Text‑to‑Speech SDK."""
        voice = (
            voice_name
            and self._find_voice(voice_name, language_code)
            or self.default_voice
        )
        input = texttospeech.SynthesisInput(text=input_text)
        voice_param = voice or self.default_voice
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        request = texttospeech.SynthesizeSpeechRequest(
            input=input, voice=voice_param, audio_config=audio_config
        )
        return self.client.synthesize_speech(request)

    def synthesize_ssml(
        self, input_ssml: str, voice_name: str = None
    ) -> texttospeech.SynthesizeSpeechResponse:
        """Synthesize SSML input using Google Cloud TTS SDK."""
        voice = voice_name and self._find_voice(voice_name) or self.default_voice
        input = texttospeech.SynthesisInput(ssml=input_ssml)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        request = texttospeech.SynthesizeSpeechRequest(
            input=input, voice=voice, audio_config=audio_config
        )
        return self.client.synthesize_speech(request)

    def _find_voice(
        self, voice_name: str, language_code: str = "en-US"
    ) -> texttospeech.VoiceSelectionParams:
        """Helper to select a voice by name or fall back to a default."""
        voices = self.client.list_voices(language_code=language_code).voices
        for v in voices:
            if v.name == voice_name:
                return texttospeech.VoiceSelectionParams(
                    language_code=language_code, name=v.name
                )
        return None  # fallback to default in parent method

    def list_voices(self, language_code: str = None) -> texttospeech.ListVoicesResponse:
        """Wrap the SDK's ListVoices call."""
        return self.client.list_voices(language_code=language_code)
