import json
from model_models import NormalizedResponse


def generate_spoken_briefing(
    response: NormalizedResponse, voice: str = "en-US"
) -> dict:
    """Create a short spoken briefing from platform output using TTS."""
    brief_text = response["content"][:120]  # truncate to a concise preview
    # Placeholder TTS – replace with real TTS API call (e.g., Azure Speech TTS)
    audio_base64 = "fake_base64_audio"
    return {
        "brief_audio": audio_base64,
        "metadata": {
            **response.get("metadata", {}),
            "briefing_generated": True,
            "voice": voice,
        },
    }
