# [LATER-STEP] reviewer_brief_audio.py
"""Generate spoken briefs for moderation reviewers using a TTS provider (e.g., ElevenLabs, Azure TTS, or OpenAI text-to-speech)."

from safety_client import get_openai_client
import base64

TTS_MODEL = 'tts-1'  # concrete provider model identifier


def generate_reviewer_brief(text: str) -> bytes:
    """Return raw audio bytes for a spoken moderation brief."""
    client = get_openai_client()
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice='alloy',
        input=text,
        response_format='mp3'
    )
    # The API returns binary MP3 data; decode to bytes
    return response.content
