# [LATER-STEP] reviewer_brief_audio.py
# Generate spoken briefs for moderation reviewers

from typing import Dict
from safety_models import SafetyResponse

# Choose ONE concrete Text-to-Speech (TTS) provider (uncomment the appropriate block in safety_client.py and import its parser)
# Example using Google Cloud Text-to-Speech (requires GOOGLE_APPLICATION_CREDENTIALS env var)

try:
    from google.cloud import texttospeech

    tts_client = texttospeech.TextToSpeechClient()
except Exception:
    # Fallback dummy that returns plain text (no spoken audio)
    def synthesize_speech(text: str, language_code: str = "en-US") -> Dict[str, str]:
        # NOTE: Replace this stub with a real TTS call in production
        return {"audio_content": b"", "audio_uri": ""}

# ---------------------------------------------------


def create_reviewer_brief(
    decision: Dict, language_code: str = "en-US"
) -> Dict[str, Any]:
    """Create an audio brief summarizing a moderation decision for a human reviewer.

    Args:
        decision: Dict containing at least 'unsafe', 'reason', and optionally 'score'.
        language_code: Language of the synthesized speech (default: English US).

    Returns:
        Dict with keys 'audio_content' (binary) and 'audio_uri' (placeholder). In a real deployment,
        'audio_content' contains synthesized WAV/MP3 and 'audio_uri' could point to a storage location.
    """
    message = f"Message {'' if decision.get('unsafe') else 'passed safety checks'}: {decision.get('reason', 'No unsafe content detected.')}."
    if decision.get("score") is not None:
        message += f" Confidence score: {decision['score']:.2f}."
    # Delegate to TTS provider
    response = synthesize_speech(message, language_code)
    return {
        "audio_content": response.get("audio_content"),
        "audio_uri": response.get("audio_uri"),
    }
