import os
from dashscope import Tts


def synthesize_text(text: str, voice: str, locale: str, output_path: str) -> bool:
    """Synthesize plain text to audio using DashScope CosyVoice.

    Returns True on success, False otherwise.
    """
    client = Tts(api_key=os.getenv("DASHSCOPE_API_KEY"))
    # Build request payload for CosyVoice (service: CosyVoice TTS)
    request = {
        "text": text,
        "format": "wav",
        "voice": voice,  # e.g., "cosy_1"
        "params": {
            "sampling_rate": 24000,
        },
    }
    try:
        response = client.tts(text=request)
        audio_bytes = response["audio"]  # binary data as bytes
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        return True
    except Exception as e:
        print(f"Synthesis error: {e}")
        return False
