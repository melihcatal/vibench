import os
import requests
from safety_models import SafetyResponse

# Generate a spoken reviewer brief using Anthropic's text-to-speech endpoint
TTS_ENDPOINT = os.getenv(
    "ANTHROPIC_SPEECH_ENDPOINT", "https://api.anthropic.com/v1/audio/tts"
)
TTS_API_KEY = os.getenv("ANTHROPIC_SPEECH_API_KEY")

TTS_ERROR = b""


def generate_reviewer_brief_audio(moderation: SafetyResponse) -> bytes:
    """Create an audio file (bytes) summarising a moderation decision for reviewer playback."""
    if not TTS_API_KEY:
        raise RuntimeError("ANTHROPIC_SPEECH_API_KEY environment variable not set")
    # Summarise for speech
    summary = (
        f"The submitted content {'' if moderation['scores'].get('TOXICITY') else 'is not '}flagged as toxic. "
        f"Detected categories: {', '.join(moderation['scores'].keys())}. "
        f"We recommend proceeding with review."
    )
    payload = {"model": "claude-3-tts-1", "input": summary, "voice": "alloy"}
    response = requests.post(
        TTS_ENDPOINT, json=payload, headers={"x-api-key": TTS_API_KEY}, timeout=10
    )
    response.raise_for_status()
    # Anthropic returns binary audio data directly
    return response.content if response.content else TTS_ERROR
