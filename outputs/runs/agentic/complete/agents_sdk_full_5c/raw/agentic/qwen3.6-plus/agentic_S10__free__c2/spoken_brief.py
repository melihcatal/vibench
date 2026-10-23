"""
Generate a spoken brief from the model output.
Provider: OpenAI - https://platform.openai.com
Model: tts-1 (openai-tts family)
API endpoint: api.openai.com/v1/audio/speech
"""

from typing import Optional, BinaryIO
import io
import os
from model_client import get_openai_client, resolve_model_family, DEFAULT_TTS_MODEL
from model_models import LLMResponse


OPENAI_TTS_VOICES = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
]

OPENAI_TTS_SPEEDS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

OPENAI_TTS_FORMATS = [
    "mp3",
    "opus",
    "aac",
    "flac",
    "wav",
    "pcm",
]


class SpokenBriefResult:
    """Result from an OpenAI Text-to-Speech API call."""

    def __init__(
        self,
        audio_data: bytes,
        model: str,
        voice: str,
        input_text: str,
        response_format: str = "mp3",
    ):
        self.audio_data = audio_data
        self.model = model
        self.voice = voice
        self.input_text = input_text
        self.response_format = response_format

    @property
    def content_type(self) -> str:
        """Return the appropriate MIME type for the audio format."""
        mime_map = {
            "mp3": "audio/mpeg",
            "opus": "audio/opus",
            "aac": "audio/aac",
            "flac": "audio/flac",
            "wav": "audio/wav",
            "pcm": "audio/pcm",
        }
        return mime_map.get(self.response_format, "application/octet-stream")

    def save_to_file(self, filepath: str) -> str:
        """Save the generated audio to a file."""
        with open(filepath, "wb") as f:
            f.write(self.audio_data)
        return filepath

    def to_fileobj(self) -> BinaryIO:
        """Return a file-like object containing the audio data."""
        return io.BytesIO(self.audio_data)

    def to_dict(self) -> dict:
        """Serialize spoken brief result metadata."""
        return {
            "model": self.model,
            "voice": self.voice,
            "format": self.response_format,
            "content_type": self.content_type,
            "audio_size_bytes": len(self.audio_data),
            "input_text_length": len(self.input_text),
            "model_family": resolve_model_family(self.model),
        }


def generate_spoken_brief(
    text: str,
    voice: str = "nova",
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    speed: float = 1.0,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> SpokenBriefResult:
    """
    Convert model output text into a spoken audio brief using the OpenAI
    text-to-speech API at api.openai.com/v1/audio/speech.

    Uses the tts-1 model with configurable voice and speed.

    Args:
        text: The text to convert to speech.
        voice: OpenAI TTS voice name (alloy, echo, fable, onyx, nova, shimmer).
        model: OpenAI TTS model (default: tts-1).
        response_format: Audio output format (mp3, opus, aac, flac, wav, pcm).
        speed: Playback speed from 0.25 to 4.0 (default: 1.0).
        api_key: Optional override for OPENAI_API_KEY.
        base_url: Optional override for OpenAI API endpoint.

    Returns:
        SpokenBriefResult containing the generated audio.
    """
    if voice not in OPENAI_TTS_VOICES:
        raise ValueError(
            f"Invalid voice '{voice}'. Choose from: {', '.join(OPENAI_TTS_VOICES)}"
        )

    client = get_openai_client(api_key=api_key, base_url=base_url)

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=speed,
    )

    audio_data = response.content

    return SpokenBriefResult(
        audio_data=audio_data,
        model=model,
        voice=voice,
        input_text=text,
        response_format=response_format,
    )


def generate_spoken_brief_from_llm_response(
    llm_response: LLMResponse,
    voice: str = "nova",
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> SpokenBriefResult:
    """
    Generate a spoken audio brief directly from an LLMResponse object,
    using OpenAI's tts-1 text-to-speech model.

    Args:
        llm_response: The LLM response containing the text to speak.
        voice: OpenAI TTS voice name.
        model: OpenAI TTS model identifier.
        response_format: Audio format.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        SpokenBriefResult with the generated speech audio.
    """
    return generate_spoken_brief(
        text=llm_response.text,
        voice=voice,
        model=model,
        response_format=response_format,
        api_key=api_key,
        base_url=base_url,
    )


def generate_spoken_brief_to_file(
    text: str,
    output_path: str,
    voice: str = "nova",
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    speed: float = 1.0,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """
    Generate spoken audio and save it to a file using OpenAI's tts-1 model.

    Args:
        text: Text to convert to speech.
        output_path: File path to save the audio.
        voice: OpenAI TTS voice name.
        model: OpenAI TTS model.
        response_format: Audio output format.
        speed: Playback speed.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        The output file path.
    """
    result = generate_spoken_brief(
        text=text,
        voice=voice,
        model=model,
        response_format=response_format,
        speed=speed,
        api_key=api_key,
        base_url=base_url,
    )
    result.save_to_file(output_path)
    return output_path


if __name__ == "__main__":
    sample_text = (
        "Here is today's brief. OpenAI has released new text-to-speech capabilities "
        "through the tts-1 model, supporting six distinct voices including nova, "
        "alloy, and shimmer. The API delivers high-quality audio output at "
        "api.openai.com."
    )

    result = generate_spoken_brief(
        text=sample_text,
        voice="nova",
        model="tts-1",
        response_format="mp3",
    )

    print(f"Model: {result.model}")
    print(f"Model family: {resolve_model_family(result.model)}")
    print(f"Voice: {result.voice}")
    print(f"Format: {result.response_format}")
    print(f"Audio size: {len(result.audio_data)} bytes")
    print(f"Content type: {result.content_type}")
    print(f"Metadata: {result.to_dict()}")

    output_path = os.path.join(os.path.dirname(__file__), "spoken_brief_output.mp3")
    saved = result.save_to_file(output_path)
    print(f"Saved to: {saved}")
