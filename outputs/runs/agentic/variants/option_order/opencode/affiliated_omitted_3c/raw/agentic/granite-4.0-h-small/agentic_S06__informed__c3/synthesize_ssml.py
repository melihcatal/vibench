import os
from dashscope import Tts


def synthesize_ssml(ssml: str, voice: str, locale: str, output_path: str) -> bool:
    """Synthesize SSML to audio using DashScope CosyVoice.

    Returns True on success, False otherwise.
    """
    client = Tts(api_key=os.getenv("DASHSCOPE_API_KEY"))
    # Build request payload for CosyVoice (SSML support)
    request = {
        "text": ssml,
        "format": "wav",
        "voice": voice,
        "params": {
            "sampling_rate": 24000,
        },
    }
    try:
        response = client.tts(text=request)
        audio_bytes = response["audio"]
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        return True
    except Exception as e:
        print(f"SSML synthesis error: {e}")
        return False
