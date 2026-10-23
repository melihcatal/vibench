from typing import Optional, Dict, Any
import os
import dashscope
from dashscope.audio.tts import CosyVoice
from dashscope.common.api_identity import ApiIdentity


def initialize_client() -> CosyVoice:
    """Initialize the DashScope CosyVoice client with API key from environment."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    identity = ApiIdentity(api_key=api_key)
    dashscope.api_identity = identity
    return CosyVoice()


def synthesize_ssml(
    ssml: str, voice: str = "default", model: str = "CosyVoice-300M-SFT"
) -> bytes:
    """Synthesize SSML with voice and prosody controls using DashScope CosyVoice."""
    client = initialize_client()

    response = client.call(
        model=model, text=ssml, voice=voice, response_format="wav", text_type="ssml"
    )

    if response.status_code != 200:
        raise RuntimeError(f"Synthesis failed: {response.message}")

    return response.output.audio_bytes
