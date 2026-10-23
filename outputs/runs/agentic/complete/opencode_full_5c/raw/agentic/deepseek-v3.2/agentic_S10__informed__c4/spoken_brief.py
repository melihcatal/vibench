import os
import dashscope
from typing import Optional


def generate_spoken_brief(
    text: str, output_file: str = "brief.mp3", voice: str = "zhiyuan"
) -> str:
    """
    Generate a spoken brief from the model output using DashScope CosyVoice TTS.
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is required")

    dashscope.api_key = api_key

    # Use CosyVoice TTS
    response = dashscope.audio.tts.SpeechSynthesizer.call(
        model="cosyvoice-v1", text=text, voice=voice, sample_rate=24000, format="mp3"
    )

    if response.status_code == 200:
        # Save audio to file
        with open(output_file, "wb") as f:
            f.write(response.output.audio)
        return output_file
    else:
        raise Exception(f"TTS failed: {response.message}")
