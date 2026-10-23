from typing import Dict, Any, Optional
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
import os


def platform_brief_audio(text: str, voice: str = "cosyvoice-1") -> Dict[str, Any]:
    """
    Generates spoken briefings from watsonx.ai model output using DashScope CosyVoice.
    Requires DASHSCOPE_API_KEY environment variable.
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY must be set.")

    dashscope.api_key = api_key

    response = SpeechSynthesizer.call(
        model="cosyvoice-v1", input={"text": text}, voice=voice, sample_rate=48000
    )

    if response.status_code != 200:
        raise RuntimeError(f"Failed to generate audio: {response.message}")

    return {
        "audio_data": response.output["audio"],
        "sample_rate": 48000,
        "voice": voice,
        "provider": "DashScope CosyVoice",
    }
