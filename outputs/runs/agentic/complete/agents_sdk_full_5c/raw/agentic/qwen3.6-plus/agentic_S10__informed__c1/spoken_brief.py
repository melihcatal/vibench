"""
Generate a spoken brief from model output using ElevenLabs Text-to-Speech.
Provider: ElevenLabs Text to Speech API
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

import os
from typing import Optional, Union, BinaryIO
from elevenlabs import ElevenLabs, Voice
from elevenlabs.client import ElevenLabs as ElevenLabsClient


# Provider-specific environment variables
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")

# Default ElevenLabs voice ID (Adam - a common male voice)
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


class ElevenLabsTTS:
    """Client for ElevenLabs Text-to-Speech API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_voice_id: str = DEFAULT_VOICE_ID,
        default_model_id: str = DEFAULT_MODEL_ID,
    ):
        self.api_key = api_key or ELEVENLABS_API_KEY
        self.default_voice_id = default_voice_id
        self.default_model_id = default_model_id
        self._client: Optional[ElevenLabsClient] = None

    @property
    def client(self) -> ElevenLabsClient:
        """Lazy-initialize the ElevenLabs SDK client."""
        if self._client is None:
            self._client = ElevenLabsClient(api_key=self.api_key)
        return self._client

    def text_to_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
        output_format: str = "mp3_44100_128",
    ) -> bytes:
        """
        Convert text to speech audio bytes.

        Args:
            text: The text to convert to speech.
            voice_id: ElevenLabs voice ID (e.g., "pNInz6obpgDQGcFmaJgB" for Adam).
            model_id: ElevenLabs model ID (e.g., "eleven_multilingual_v2").
            output_format: Audio output format.

        Returns:
            Audio bytes in the specified format.
        """
        vid = voice_id or self.default_voice_id
        mid = model_id or self.default_model_id

        audio = self.client.generate(
            text=text,
            voice=vid,
            model=mid,
            output_format=output_format,
        )
        return b"".join(audio)

    def text_to_speech_stream(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> BinaryIO:
        """
        Stream text-to-speech audio.

        Args:
            text: The text to convert.
            voice_id: ElevenLabs voice ID.
            model_id: ElevenLabs model ID.

        Returns:
            BinaryIO stream of audio data.
        """
        vid = voice_id or self.default_voice_id
        mid = model_id or self.default_model_id

        return self.client.generate(
            text=text,
            voice=vid,
            model=mid,
            stream=True,
        )

    def list_voices(self) -> list:
        """List available ElevenLabs voices."""
        voices = self.client.voices.get_all()
        return [
            {
                "voice_id": v.voice_id,
                "name": v.name,
                "category": v.category,
            }
            for v in voices.voices
        ]


def generate_spoken_brief(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = DEFAULT_MODEL_ID,
    output_path: Optional[str] = None,
) -> Union[bytes, str]:
    """
    Generate a spoken brief from text output.

    Args:
        text: The text to convert to speech.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs TTS model ID.
        output_path: Optional file path to save the audio.

    Returns:
        Audio bytes, or the output path if saved to file.
    """
    tts = ElevenLabsTTS()
    audio_bytes = tts.text_to_speech(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
    )

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        return output_path

    return audio_bytes


if __name__ == "__main__":
    if not ELEVENLABS_API_KEY:
        print("ELEVENLABS_API_KEY environment variable is required.")
    else:
        tts = ElevenLabsTTS()
        sample_text = "Hello, this is a spoken brief generated using ElevenLabs text-to-speech."
        print(f"Generating speech for: {sample_text}")
        audio = tts.text_to_speech(sample_text)
        print(f"Generated audio: {len(audio)} bytes")
