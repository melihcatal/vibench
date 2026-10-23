import os
import random
from textwrap import dedent
from translation_models import TranslateRequest, TranslateResponse, NormalizedResponse
from translation_memory_embedding import embed_translation_segment

TTS_SERVICE = "dashscope_cosyvoice"
TTS_ENDPOINT = "https://api.example.com/tts"  # placeholder URL
TTS_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not TTS_API_KEY:
    raise RuntimeError("DASHSCOPE_API_KEY not configured")


def synthesize_audio_for(text: str, language: str = "en") -> bytes:
    """Generate a spoken audio preview of the translated text."""
    headers = {
        "Authorization": f"Bearer {TTS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice": "zh-cn-kano",
        "language": language,
        "speed": 1.0
    }
    try:
        resp = requests.post(TTS_ENDPOINT, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.content  # raw audio bytes (e.g., MP3 or WAV)
    except Exception as e:
        print(f"Audio synthesis error: {e}")
        return b""


def preview_translated_copy(translated_segments: List[str], language: str = "en") -> List[bytes]:
    """Create audio previews for each translated segment and return raw audio blobs."""
    audios = []
    for seg in translated_segments:
        audio = synthesize_audio_for(seg, language)
        audios.append(audio)
    return audios

# Example usage (remove in production)
if __name__ == "__main__":
    sample = "Welcome to our service!"
    embed = embed_translation_segment(sample)
    print("Embedding result:", embed)
    preview = preview_translated_copy([sample], language="es")[0]
    print(f"Audio preview length: {len(preview)} bytes")
