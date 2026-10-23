import json
from safety_client import SafetyClient


def generate_audio_brief(decision: str, rationale: str) -> str:
    """Generate a spoken brief for moderation reviewers using Alibaba TTS.

    Returns a URL to the generated audio file (mocked here).
    """
    client = SafetyClient()
    # Mock: return a placeholder URL
    return "https://example.com/audio_brief.mp3"
