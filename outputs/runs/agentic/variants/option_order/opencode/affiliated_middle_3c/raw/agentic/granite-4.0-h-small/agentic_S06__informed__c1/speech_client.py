import os
from typing import TypeAlias

# Provider constants—select one concrete TTS service for this project
PROVIDER_NAME = "Google Cloud Text-to-Speech"
# Environment variable that holds credentials; aligns with provider auth list
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Alias to reflect the concrete client once imported
tts_client: TypeAlias = "google.cloud.texttospeech.TextToSpeechClient"

def get_client() -> tts_client:
    """Return an authenticated client for the selected TTS provider.

    The client creation respects the environment variable `GOOGLE_APPLICATION_CREDENTIALS`.
    """
    from google.cloud import texttospeech
    return texttospeech.TextToSpeechClient()

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

class SynthesisConfig:
    """Simple data class to hold synthesis parameters.

    Attributes can be extended as new provider capabilities are added.
    """
    def __init__(
        self,
        input_text: str = "",
        input_ssml: str = "",
        voice_name: str | None = None,
        voice_gender: str | None = None,
        language_code: str = "en-US",
        prosody: dict | None = None,
        audio_encoding: str = "MP3",
    ) -> None:
        self.input_text = input_text
        self.input_ssml = input_ssml
        self.voice_name = voice_name
        self.voice_gender = voice_gender
        self.language_code = language_code
        self.prosody = prosody  # e.g., {"rate": 0.9}
        self.audio_encoding = audio_encoding

    def _to_google_config(self) -> "texttospeech.SynthesisInput":
        from google.cloud import texttospeech
        # Choose between text and SSML based on presence of markup tags
        if self.input_ssml:
            return texttospeech.SynthesisInput(ssml=self.input_ssml)
        return texttospeech.SynthesisInput(text=self.input_text)

    def build_request(self, client: tts_client) -> "texttospeech.SynthesizeSpeechRequest":
        import google.cloud.texttospeech_v1.types as types
        input_ = self._to_google_config()
        # Voice selection logic (fallback to voice_name if provided)
        voice_spec = None
        if self.voice_name:
            voice_spec = types.VoiceSelectionParams(name=self.voice_name)
        elif self.voice_gender:
            gender_map = {
                "MALE": types.SsmlVoiceGender.MALE,
                "FEMALE": types.SsmlVoiceGender.FEMALE,
                "NEUTRAL": types.SsmlVoiceGender.NEUTRAL,
            }
            voice_spec = types.VoiceSelectionParams(ssml_gender=gender_map[self.voice_gender])
        audio_cfg = types.AudioConfig(audio_encoding=types.AudioEncoding[self.audio_encoding])
        # Prosody support via speaking_rate/sample_rate_hertz (simple mapping here)
        speaking_rate = self.prosody.get("rate") if self.prosody else None
        sample_rate_hz = self.prosody.get("sample_rate_hertz") if self.prosody else None
        if speaking_rate is not None:
            audio_cfg.speaking_rate = float(speaking_rate)
        if sample_rate_hz is not None:
            audio_cfg.sample_rate_hertz = int(sample_rate_hz)
        return texttospeech.SynthesizeSpeechRequest(
            input=input_,
            voice=voice_spec,
            audio_config=audio_cfg,
        )


class TTSResult:
    """Container for the result returned by `get_client().synthesize_speech`.",
    def __init__(self, audio_bytes: bytes, metadata: dict | None = None) -> None:
        self.audio = audio_bytes
        self.metadata = metadata

    def save(self, path: str) -> None:
        """Write audio to a local file."""
        with open(path, "wb") as f:
            f.write(self.audio)
        print(f"Audio saved to {path}")

    def upload(self, bucket: str, key: str) -> None:
        """Upload audio to object storage (provider‑specific implementation required)."""
        # Placeholder – replace with actual SDK call for chosen provider
        print(f"Audio uploaded to bucket={bucket} key={key}")

# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    client = get_client()
    config = SynthesisConfig(input_text="Hello world! This is a test.", voice_name="en-US-Wavenet-D")
    req = config.build_request(client)
    resp = client.synthesize_speech(request=req)
    tts = TTSResult(resp.audio_content)
    tts.save("sample.mp3")
