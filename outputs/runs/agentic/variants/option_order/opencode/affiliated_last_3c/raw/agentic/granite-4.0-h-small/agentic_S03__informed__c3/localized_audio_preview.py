import os

try:
    from edge_impulse_sdk import EdgeImpulse  # Using Edge Impulse TTS as example
except ImportError:
    raise ImportError("Install Edge Impulse SDK: pip install edge-impulse-sdk")

# Load credentials from environment (Edge Impulse)
EDGE_IMPULSE_API_KEY = os.getenv("EDGE_IMPULSE_API_KEY")
if not EDGE_IMPULSE_API_KEY:
    raise RuntimeError("Set EDGE_IMPULSE_API_KEY environment variable")

tts = EdgeImpulse(api_key=EDGE_IMPULSE_API_KEY)


def generate_audio_preview(text: str, language: str = "en") -> bytes:
    """Generate spoken audio preview of translated copy using Edge Impulse TTS.

    Args:
        text (str): Text to synthesize.
        language (str): Language code for synthesis (default "en").

    Returns:
        bytes: Raw audio bytes (e.g., WAV format).
    """
    return tts.synthesize(text=text, language=language)
