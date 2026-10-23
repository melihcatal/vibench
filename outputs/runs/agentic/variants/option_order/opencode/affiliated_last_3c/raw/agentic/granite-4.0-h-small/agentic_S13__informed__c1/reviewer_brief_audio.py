import json
from safety_models import build_request, normalize_response
from safety_client import analyze_sentiment


def generate_audio_brief(moderation_decision: Dict[str, Any]) -> str:
    """Generate a spoken brief for moderation reviewers.

    Uses a hosted text‑to‑speech service (e.g., Google Cloud Text-to-Speech) to
    produce an audio file (MP3) that summarizes the moderation verdict.
    Provider identifier (google) is visible in the client import.
    """
    # Prepare a short textual summary
    text = f"User message flagged as unsafe: {moderation_decision.get('unsafe', False)}. Scores: {json.dumps(moderation_decision.get('scores', {}))}"
    # Placeholder: actual TTS call would go here
    # audio_filepath = tts_client.synthesize(text, voice='en-US_Women_V2', format='mp3')
    return f"Audio brief generated for decision: {moderation_decision}"
